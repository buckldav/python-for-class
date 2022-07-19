import os
from pprint import pprint
from traceback import print_exception
import xml.etree.ElementTree as ET
from uuid import uuid4
import zipfile
import csv
import json

CSV_FILENAME = "questions.csv"


def ident():
    """
    Random UUID string that satisfies the regex: s/i(\d|[a-f]){32}/g.
    """
    return "i" + uuid4().__str__().replace("-", "")


def ans_id(q_num: int, a_num: int):
    """
    Question 1, Answer 2: 1002
    Question 3, Answer 1: 30001
    """
    return str(q_num) + str(a_num).zfill(3)


def create_base_doc():
    """
    <?xml version="1.0" encoding="ISO-8859-1"?>
    <questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
      <assessment ident="ibc9e6c0dda46d98271b7f3f528d1fd33" title="Quiz_Import_Example_Revised2">
        <qtimetadata>
          <qtimetadatafield>
            <fieldlabel>cc_maxattempts</fieldlabel>
            <fieldentry>1</fieldentry>
          </qtimetadatafield>
        </qtimetadata>
        <section ident="root_section">
            ...
        </section>
      </assessment>
    </questestinterop>
    """
    qti = ET.Element(
        "questestinterop",
        {
            "xmlns": "http://www.imsglobal.org/xsd/ims_qtiasiv1p2",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd",
        },
    )
    asmt = ET.SubElement(
        qti,
        "assessment",
        {"ident": ident(), "title": CSV_FILENAME.removesuffix(".csv")},
    )
    qtime = ET.SubElement(asmt, "qtimetadata")
    qtdfield = ET.SubElement(qtime, "qtimetadatafield")
    ET.SubElement(qtdfield, "fieldlabel").text = "cc_maxattempts"
    ET.SubElement(qtdfield, "fieldentry").text = "1"
    root = ET.SubElement(asmt, "section", {"ident": "root_section"})

    return qti, root


def create_q(
    root: ET.Element,
    q_num: int,
    points: float,
    q_body: str,
    answers: list[str],
    correct_indicies: list[int],
):
    """
    Create the XML for a single multiple choice or multiple response question.
    """
    is_mcq = len(correct_indicies) == 1
    q_type = "multiple_choice_question" if is_mcq else "multiple_answers_question"
    r_cardinality = "Single" if is_mcq else "Multiple"
    response_lid = "response1"

    def mcq_scoring(conditionvar: ET.Element):
        """
        Create the XML for a multiple choice question's scoring.
        """
        ET.SubElement(
            conditionvar, "varequal", {"respident": response_lid}
        ).text = ans_id(q_num, correct_indicies[0])

    def mrq_scoring(conditionvar: ET.Element, num_answers: int):
        """
        Create the XML for a multiple response question's scoring.
        """
        and_el = ET.SubElement(conditionvar, "and")
        for i in range(num_answers):
            parent = and_el
            if not i in correct_indicies:
                parent = ET.SubElement(and_el, "not")
            ET.SubElement(
                parent, "varequal", {"respident": response_lid}
            ).text = ans_id(q_num, i)

    item = ET.SubElement(root, "item", {"ident": ident(), "title": f"Question {q_num}"})

    # metadata
    imd = ET.SubElement(item, "itemmetadata")
    qtimd = ET.SubElement(imd, "qtimetadata")
    md_items = [
        ("question_type", q_type),
        ("points_possible", str(points)),
        ("assessment_question_identifierref", ident()),
    ]
    for i in md_items:
        qtimdf = ET.SubElement(qtimd, "qtimetadatafield")
        ET.SubElement(qtimdf, "fieldlabel").text = i[0]
        ET.SubElement(qtimdf, "fieldentry").text = i[1]

    # choices
    presentation = ET.SubElement(item, "presentation")
    material = ET.SubElement(presentation, "material")
    ET.SubElement(material, "mattext", {"texttype": "text/html"}).text = q_body
    res_lid_el = ET.SubElement(
        presentation,
        "response_lid",
        {"ident": response_lid, "rcardinality": r_cardinality},
    )
    rc = ET.SubElement(res_lid_el, "render_choice")
    for i, a in enumerate(answers):
        rlabel = ET.SubElement(rc, "response_label", {"ident": ans_id(q_num, i)})
        mat = ET.SubElement(rlabel, "material")
        ET.SubElement(mat, "mattext", {"texttype": "text/plain"}).text = a

    # scoring
    resprocessing = ET.SubElement(item, "resprocessing")
    outcomes = ET.SubElement(resprocessing, "outcomes")
    ET.SubElement(
        outcomes,
        "decvar",
        {"maxvalue": "100", "minvalue": "0", "varname": "SCORE", "vartype": "Decimal"},
    )
    respcondition = ET.SubElement(resprocessing, "respcondition", {"continue": "No"})
    conditionvar = ET.SubElement(respcondition, "conditionvar")

    if is_mcq:
        mcq_scoring(conditionvar)
    else:
        mrq_scoring(conditionvar, len(answers))

    ET.SubElement(
        respcondition, "setvar", {"action": "Set", "varname": "SCORE"}
    ).text = "100"


def create_qs_from_csv(root, filename):
    """
    Creates questions from a CSV file.

    Example CSV file:
    5,"This is <strong>question 1</strong>","[""a"", ""b"", ""c"", ""d""]","[2]"
    2,"This is <strong>question 2</strong>","[""a"", ""b"", ""c"", ""d""]","[1, 3]"
    """
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for q_num, row in enumerate(reader):
            points = row[0]
            q_body = row[1]
            answers = ""
            correct_indicies = []
            try:
                answers = json.loads(row[2])
            except Exception as e:
                print_exception(e)
            try:
                correct_indicies = json.loads(row[3])
            except Exception as e:
                print_exception(e)

            create_q(root, q_num + 1, points, q_body, answers, correct_indicies)


def write_to_file(qti: ET.Element, filename: str, delete=True):
    """
    Write the XML to a file and put it in a zip folder. The zip folder is what gets uploaded to Canvas.

    :param ET.Element qti: The root XML element of the QTI-formatted XML document.
    :param str filename: The filename is extension-less.
    :param bool delete: Delete the XML file that is not in the zip folder.
    """
    tree = ET.ElementTree(qti)
    xmlfile = filename + ".xml"
    with open(xmlfile, "wb") as f:
        tree.write(f, "ISO-8859-1")
        zf = zipfile.ZipFile(filename + ".zip", "w")
        zf.write(xmlfile)
    if delete:
        os.remove(xmlfile)


if __name__ == "__main__":
    qti, root = create_base_doc()
    create_qs_from_csv(root, CSV_FILENAME)
    write_to_file(qti, CSV_FILENAME.removesuffix(".csv"))

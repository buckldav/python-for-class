# Adapted from http://kazuar.github.io/scraping-tutorial/
import requests
import csv
import os
from datetime import datetime
from pytz import timezone
from lxml import html
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

USERNAME = os.getenv("CODEHS_USERNAME")
PASSWORD = os.getenv("PASSWORD")

LOGIN_URL = "https://codehs.com/login"

def get_students(session_requests):
    URL = "https://codehs.com/section/160503/course/1939/"
    result = session_requests.get(URL, headers = dict(referer = URL))
    tree = html.fromstring(result.content)
    f = open("scrapedpage.html", "w")
    f.write(result.text.__str__())

    student_names = tree.xpath("//div[@class='students table']/div[@class='row']/h1/text()")
    student_info = tree.xpath("//div[@class='students table']/div[@class='row']/a[@class='link-wrapper']")
    students = [ { "name": student_names[i], "url": "https://codehs.com" + student_info[i].get('href') } for i in range(len(student_names)) ]
    return students

def get_student_results(student, session_requests, writer):
    result = session_requests.get(student['url'], headers = dict(referer = student['url']))
    tree = html.fromstring(result.content)

    lesson_names = tree.xpath("//div[@class='module-title']/text()")
    lesson_names = [ name.__str__().strip() for name in lesson_names if name.__str__().strip() != '' ]
    lesson_percentage = tree.xpath("//div[@class='module-info-right']/div/text()")
    lesson_percentage = [ pct.__str__().strip() for pct in lesson_percentage if pct.__str__().strip() != '' ]
    
    print("Scoring", student['name'], "...")
    writer.writerow([name for name in student['name'].split()])
    for i in range(len(lesson_percentage)):
        writer.writerow([lesson_names[i], lesson_percentage[i]])
    writer.writerow([])

def main():
    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]

    # Create payload
    payload = {
        "email": USERNAME, 
        "password": PASSWORD, 
        "csrfmiddlewaretoken": authenticity_token
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Scrape url
    students = get_students(session_requests)

    # Iterate through each student and grab data
    with open(f"codehs{datetime.now(timezone('US/Mountain')).strftime('%Y-%m-%d %H%M%S')}.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for student in students:
            get_student_results(student, session_requests, writer)

if __name__ == '__main__':
    main()
import csv

FILENAME = "emails.csv"
TECH_STUDENTS = []
   
def makeEmails(names):
  emails = []
  #names.sort()
  for name in names:
    nameArr = name.lower().split()
    # If 4 items, get rid of latino middlename
    # Example: Brad *Bradson* Avila 2013
    if len(nameArr) == 4:
      nameArr[1] = nameArr[2]
    # Check for hyphen in lastname, get rid of first half
    # Example: Brad *Bradson-*Avila 2013
    hyphenArr = nameArr[1].split("-")
    nameArr[1] = hyphenArr[len(hyphenArr) - 1]
    # Generate Email
    email = nameArr[0] + "." + nameArr[1] + "@meritknights.com"
    emails.append([name, email])

  return emails

STUDENTS = []
with open('active_students.csv') as csvfile:
  csvRead = csv.reader(csvfile, delimiter=',')
  for row in csvRead:
    STUDENTS.append(row[0].split("Â")[0])

emailFile = open(FILENAME, 'w', newline='')
emails = makeEmails(STUDENTS)

with emailFile:
  writer = csv.writer(emailFile)
  writer.writerows(emails)

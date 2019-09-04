import csv

FILENAME = "emails.csv"
STUDENTS = [
  "Kyler Day",
  "Bryson Day",
  "Christopher Johnson",
  "Carter Cook",
  "Joseph Henage",
  "Dallin Charbonneau",
  "Ryan Meeks",
  "Charles Kidder",
  "Raven Kinsman",
  "Max Wenham",
  "Jaron Siebach",
  "Michael Dyck",
  "Richard Henage",
  "Luke Eddy",
  "Adam Jenkins",
  "Isaac Jensen",
  "Bryson Day",
  "Joseph Wiseman",
  "Eduardo Gutierrez",
  "Owen Healy",
  "Wyatt Hendricks"
]
   
def makeEmails(names):
  emails = []
  names.sort()
  for name in names:
    nameArr = name.lower().split()
    email = nameArr[0] + "." + nameArr[1] + "@meritknights.com"
    emails.append([name, email])

  return emails

emailFile = open(FILENAME, 'w', newline='')
emails = makeEmails(STUDENTS)
with emailFile:
  writer = csv.writer(emailFile)
  writer.writerows(emails)

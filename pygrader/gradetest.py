# Works with the ZipGrade app, formats an exported .csv file into something more printable
import csv
from random import randrange

FILES = ["prog1.csv"]

for filename in FILES:
   myFile = open(filename, 'r', newline='')  
   with myFile:  
      reader = csv.reader(myFile)

      header = []
      for row in reader:
        header = row
        break
      
      for row in reader:
        # If the row is not empty
        if row[0] != "":
          # Make a file with the student's name
          newFile = open(row[2].lower() + '_' + row[3].lower().replace(" ", "_") + ".csv", 'w', newline='')
          with newFile:
            writer = csv.writer(newFile)
            # Put the metadata at the top
            writer.writerows([header[0:7], row[0:7]])
            # Make a row for each question/answer
            for i in range(8, len(header), 3):
              writer.writerows([header[i:i+3], row[i:i+3]])

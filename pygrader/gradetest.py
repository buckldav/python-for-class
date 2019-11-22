import csv
from random import randrange

FILES = ["prog1.csv"]
LENGTHS = []

for filename in FILES:
   myFile = open(filename, 'r', newline='')  
   with myFile:  
      reader = csv.reader(myFile)

      header = []
      for row in reader:
        header = row
        break
      
      for row in reader:
        if row[0] != "":
          newFile = open(row[2].lower() + '_' + row[3].lower().replace(" ", "_") + ".csv", 'w', newline='')
          with newFile:
            writer = csv.writer(newFile)
            writer.writerows([header[0:7], row[0:7]])
            for i in range(8, len(header), 3):
              writer.writerows([header[i:i+3], row[i:i+3]])

  #  sortedFile = open("analyzed_" + filename, 'w', newline='')
  #  with sortedFile:
  #     writer = csv.writer(sortedFile)
  #     writer.writerows(sorted(myData))

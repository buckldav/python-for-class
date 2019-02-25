import csv
from random import randrange

FILES = ["key.csv", "student1.csv", "student2.csv", "student3.csv", "student4.csv", "student5.csv"]
ANSWERS = ["A", "B", "C", "D"]

def generateData(filename):
   data = []
   data.append([filename[:-4]])
   for i in range(20):
      data.append([str(i+1), ANSWERS[randrange(0, 4)]])
   return data

def grade(key, toGrade, result):
   score = 0
   maxScore = 0
   for keyLine, gradeLine in zip(key, toGrade):
      if len(keyLine) > 1:
         maxScore += 1
         if keyLine[1] == gradeLine[1]:
            score += 1
   result.append([toGrade[0][0], str(score*100/maxScore)+"%"])
   

key = []
gradeResult = []
for filename in FILES:
   myData = generateData(filename)
   myFile = open(filename, 'w', newline='')  
   with myFile:  
      writer = csv.writer(myFile)
      writer.writerows(myData)

   # Grade the work
   if filename == "key.csv":
      key = myData
   else:
      grade(key, myData, gradeResult)

# Make the graded file
gradedFile = open("graded.csv", 'w', newline='')
with gradedFile:
   writer = csv.writer(gradedFile)
   writer.writerows(gradeResult)

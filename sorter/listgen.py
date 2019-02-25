import csv
from random import randrange

FILES = ["list1.csv", "list2.csv", "list3.csv", "list4.csv"]
LENGTHS = [5, 20, 100, 1000]

def generateData(filename, length):
   data = []
   for i in range(length):
      data.append([(randrange(0, 5000))])
   return data

i = 0
for filename in FILES:
   myData = generateData(filename, LENGTHS[i])
   myFile = open(filename, 'w', newline='')  
   with myFile:  
      writer = csv.writer(myFile)
      writer.writerows(myData)

   sortedFile = open("sorted_" + filename, 'w', newline='')
   with sortedFile:
      writer = csv.writer(sortedFile)
      writer.writerows(sorted(myData))

   i += 1
import random


def studentsPerGroup(students):
    # Get factors of len(students) excluding 1 and self
    # The factors are the allowable number of groups
    factors = []
    for i in range(2, len(students)):
        if len(students) % i == 0:
            factors.append(i)
    n = ""
    while True:
        n = input("Number of groups: " + str(factors) +
                  "\nFor random student, type 'r': ")
        if n == "r":
            print("\nRandom student: " +
                  students[random.randint(0, len(students) - 1)] + "!\n")
            return 0  # No groups needed
        for i in range(0, len(factors)):
            if str(factors[i]) == n:
                return len(students) // int(n)  # Number of students per group


def main():
    print()
    students = [
        "Zayne",
        "Eliot",
        "Owen",
        "Glen",
        "Jonas",
        "Amy",
        "Isaac",
        "Lucy",
        "Gavin",
        "Veronica",
        "Eleanor",
        "Neeve",
        "Abby",
        "EJ",
        "Noah",
        "Jackson",
        "Ty",
        "Logan"
    ]  # TODO
    random.shuffle(students)
    n = studentsPerGroup(students)
    if n != 0:
        min = 0
        max = n
        groupNumber = 1
        while max <= len(students):
            print("\nGroup " + str(groupNumber) + ":")
            for i in range(min, max):
                if students[i] != "":
                    print(" " + students[i])
            min = max
            max += n
            groupNumber += 1
        print()


a = ""
while a == "":
    main()
    a = input("Press enter to continue, type any key to exit")

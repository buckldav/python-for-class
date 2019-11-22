score = 0
def checkAnswer(correct, user):
  global score
  if correct.lower() == user.lower():
    print("Correct!")
    score += 1
  else:
    print("Incorrect! The correct answer was: " + correct)
  print("Score: " + str(score))

print("Question 1: What are the bones in the middle of your foot called?")
checkAnswer("Metatarsals", input())
print("Question 2: What are the bones in the middle of your hand called?")
checkAnswer("Metacarpals", input())
print("Question 3: What is the longest bone in the body?")
checkAnswer("Femur", input())

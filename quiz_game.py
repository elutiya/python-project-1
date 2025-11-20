# 5. Quiz Game
# Create a basic quiz game that:
# Contains a list of 5–10 questions stored in a dictionary (or list of dicts).
# Asks the user each question and records their answers.
# At the end, displays:
# The user’s score (e.g., 7/10)
# Correct answers for any questions they got wrong
# Skills practiced: loops, dictionaries, input, comparison, counters, print formatting


quiz = [
         {"question" : "what is the capital city of USA",
          "options":["A. LA",  "B. DC",  "C, MA "],
          "answer": "B"},
        { "question" : "what is the capital city of canada",
          "options":["A. LA",  "B. DC",  "C, MA "],
          "answer": "B"},
        { "question" : "what is the capital city of france",
          "options":["A. LA",  "B. DC",  "C, MA "],
          "answer": "B"}
        ]
wrong_answers=[]
score = 0
for x in quiz:
  print(f"{x['question']}")
  for option in x['options']:
    print(option)
  answer = input("what is your answer:- ").upper()
  if answer == x['answer']:
   print("Right!\n")
   score+=1
  else:
   print("Wrong!\n")
   wrong_answers.append((x['question'], x['answer']))
print(f"You got {score}/{len(quiz)} correct!\n")
if wrong_answers:
    print("Here are the correct answers for the questions you missed:")
    for question, correct in wrong_answers:
        print(f"- {question} (Answer: {correct})")
else:
    print("Perfect score!  Great job!")
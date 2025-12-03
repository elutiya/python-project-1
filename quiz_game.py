# 5. Quiz Game
# Create a basic quiz game that:

#     Contains a list of 5–10 questions stored in a dictionary (or list of dicts).
#     Asks the user each question and records their answers.
#     At the end, displays:
#         The user’s score (e.g., 7/10)
#         Correct answers for any questions they got wrong
# > Skills practiced: loops, dictionaries, input, comparison, counters, print formatting

import time
import random
import os
import sys

from colorama import Fore, Style, init
init(autoreset=True)

def load_questions_from_file(filename="questions.txt"):

    questions = []
    if not os.path.exists(filename):
        print(f"Questions file '{filename}' not found. Using empty question set.")
        return questions
    with open(filename, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) < 2:
                print(f"Skipping malformed line {lineno} in {filename}: {line}")
                continue
            question = parts[0].strip()
            answer = parts[1].strip()
            choices = None
            hint = None
            if len(parts) >= 3 and parts[2].strip():
                choices = [c.strip() for c in parts[2].split(";") if c.strip()]
            if len(parts) >= 4:
                hint = parts[3].strip()
            q = {"question": question, "answer": answer}
            if choices:
                q["choices"] = choices
            if hint:
                q["hint"] = hint
            questions.append(q)
    return questions


def get_remaining_indices(total, asked_indices):
    return [i for i in range(total) if i not in asked_indices]

def get_round_indices(total, asked_indices, n=5):
    remaining = get_remaining_indices(total, asked_indices)
    if len(remaining) < n:
        return remaining
    return random.sample(remaining, n)

def mark_asked(asked_indices, indices):
    asked_indices.update(indices)

def reset_asked():
    return set()


def timed_input(prompt):
    return input(prompt)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


CYAN = Fore.CYAN + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
BLUE = Fore.BLUE + Style.BRIGHT
END = Style.RESET_ALL
HEADER_BG = "\033[48;2;10;25;47m" + Fore.WHITE + Style.BRIGHT
QUESTION_BG = "\033[48;2;60;40;90m" + Fore.WHITE + Style.BRIGHT
CHOICE_BG = "\033[48;2;230;230;235m" + Fore.BLACK + Style.NORMAL


def loading_animation(duration=1.2):
    print(CYAN + "Processing", end="")
    steps = max(1, int(duration / 0.3))
    for _ in range(steps):
        for dot in range(1, 4):
            print(CYAN + "." * dot, end="\r")
            time.sleep(0.3)
    print(" " * 20, end="\r")


def ask_question(q_dict, q_no=1, total_q=1):
    clear_screen()
    original_choices = q_dict.get("choices") or []
    display_choices = list(original_choices)
    if display_choices:
        random.shuffle(display_choices)
    choices_list = [f"{idx}. {c}" for idx, c in enumerate(display_choices, 1)]
    question_text = q_dict["question"]
    header_text = f"Question {q_no}/{total_q}"
    content_width = max(len(question_text), max((len(s) for s in choices_list), default=0), len(header_text))
    box_width = max(content_width, 40)

    print(HEADER_BG + f" {header_text.ljust(box_width)} " + END)
    print(QUESTION_BG + f" {question_text.ljust(box_width)} " + END)
    if display_choices:
        for idx, choice in enumerate(display_choices, 1):
            choice_str = f"{idx}. {choice}"
            print(CHOICE_BG + f" {choice_str.ljust(box_width)} " + END)

    print(YELLOW + "Type your answer. Type 'hint' to request a hint (costs 2 points)." + END)

    hint_used = False
    while True:
      user_answer = timed_input(YELLOW + "Your answer: " + END)
      if user_answer == "" :
                print("please enter the answer")
                continue
      else:
          break
    
    answered = False

    # If the player asked for a hint
    if user_answer.strip().lower() == "hint":
        if "hint" in q_dict:
            print(GREEN + f"Hint: {q_dict['hint']}" + END)
            hint_used = True
            loading_animation(0.6)
            print(YELLOW + "Type your answer:" + END)
            user_answer = timed_input("")
            if not user_answer.strip():
                print(RED + "No answer provided after hint." + END)
                return False, False, hint_used
            answered = True
        else:
            print(RED + "No hint available for this question." + END)
            user_answer = timed_input("")
            if not user_answer.strip():
                print(RED + "No answer provided." + END)
                return False, False, hint_used
            answered = True

    else:
        if not user_answer.strip():
            print(RED + "No answer provided." + END)
            return False, False, hint_used
        answered = True

    if display_choices:
        while True:
            if user_answer.strip().isdigit():
                idx = int(user_answer) - 1
                if 0 <= idx < len(display_choices):
                    user_answer = display_choices[idx]
                    break
                else:
                    print(RED + f"Please enter a number between 1 and {len(display_choices)}." + END)
            
            else:
                print(RED + "Invalid input. Please enter the number of your choice." + END)
            
            user_answer = timed_input(YELLOW + "Your answer: " + END)




    correct_answer = q_dict["answer"].strip().lower()
    if user_answer.strip().lower() == correct_answer:
        print(GREEN + "Correct!" + END)
        return True, True, hint_used
    else:
        print(RED + f"Incorrect. The correct answer was: {q_dict['answer']}\n" + END)
        return False, True, hint_used

def save_high_score(name, score, percent):
    filename = "highscores.txt"
    with open(filename, "a") as f:
        f.write(f"{name},{score},{percent:.2f}%\n")

def show_high_scores():
    filename = "highscores.txt"
    if not os.path.exists(filename):
        print("No high scores yet.")
        return
    print("\nHigh Scores:")
    with open(filename) as f:
        for line in f:
            print(line.strip())

def run_quiz(questions, asked_indices, per_round=5):
    total = len(questions)
    if total == 0:
        print("No questions available. Please add questions to 'questions.txt'.")
        return
    indices = get_round_indices(total, asked_indices, per_round)
    if len(indices) < per_round:
        remaining = len(indices)
        print(f"Only {remaining} new question(s) remaining that haven't been asked yet.")
        choice = input("Would you like to reset the asked questions and continue? (yes/no): ").strip().lower()
        if choice == "yes":
            asked_indices.clear()
            indices = get_round_indices(total, asked_indices, per_round)
    if len(indices) == 0:
        print("No questions available for this round.")
        return
    if len(indices) > per_round:
        indices = indices[:per_round]
    mark_asked(asked_indices, indices)
    score = 0
    correct_count = 0
    wrong_count = 0
    wrong_answers = []
    print("Welcome to the Quiz!\n")
    for pos, i in enumerate(indices, start=1):
        q_dict = questions[i]
        correct, answered, hint_used = ask_question(q_dict, q_no=pos, total_q=len(indices))
        if correct:
            points = 3 if hint_used else 5
            score += points
            correct_count += 1
            print(GREEN + f"You earned {points} points for this question." + END)
        elif answered:
            wrong_count += 1
            wrong_answers.append(q_dict)
        else:
            print("No answer or time expired. Moving to next question.\n")
            wrong_count += 1
            wrong_answers.append(q_dict)
    print("You Have Finished The Quiz!")
    print(f"Your final score is: {score}/{len(indices)*5}")
    percent = (score / (len(indices)*5)) * 100
    print(f"Score breakdown: Correct: {correct_count}, Incorrect: {wrong_count}")
    print(f"Percentage score: {percent:.2f}%")
    if wrong_answers:
        print("\nHere are the questions you got wrong:")
        for q_dict in wrong_answers:
            print(f"  Question: {q_dict['question']}")
            print(f"  Answer: {q_dict['answer']}\n")
    else:
        print("\nWow, you got all the questions right!")
    name = input("Enter your name for the high score list: ").strip()
    save_high_score(name, score, percent)
    show_high_scores()


def main():
    questions = load_questions_from_file("questions.txt")
    asked_indices = set()
    while True:
        run_quiz(questions, asked_indices, per_round=5)
        replay = input("Would you like to play another round? (yes/no): ").strip().lower()
        if replay != "yes":
            print("Thanks for playing!")
            break

try:
    main()
except (KeyboardInterrupt, EOFError):
    print("\n\nExiting quiz. Goodbye.")
    sys.exit(0)

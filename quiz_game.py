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
import signal

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


def timed_input(prompt, timeout):
    def _handler(signum, frame):
        raise TimeoutError
    old_handler = signal.signal(signal.SIGALRM, _handler)
    signal.alarm(timeout)
    try:
        return input(prompt)
    except TimeoutError:
        return None
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


def ask_question(q_dict, time_limit=15, extra_time_with_hint=10):
    print(q_dict["question"])
    if "choices" in q_dict:
        for idx, choice in enumerate(q_dict["choices"], 1):
            print(f"  {idx}. {choice}")
    print(f"You have {time_limit} seconds to answer.")
    user_answer = timed_input("Your answer: ", time_limit)
    answered = False
    if user_answer is None:
        print("Time's up!")
        if "hint" in q_dict:
            want_hint = input("Would you like a hint? (yes/no): ").strip().lower()
            if want_hint == "yes":
                print(f"Hint: {q_dict['hint']}")
                user_answer = timed_input(f"You have {extra_time_with_hint} seconds to answer: ", extra_time_with_hint)
                if user_answer is None:
                    print("No answer provided after hint.")
                    return False, False
                answered = True
            else:
                return False, False
        else:
            return False, False
    else:
        answered = True
        
    if "choices" in q_dict and user_answer is not None:
        if user_answer.strip().isdigit():
            idx = int(user_answer.strip()) - 1
            if 0 <= idx < len(q_dict["choices"]):
                user_answer = q_dict["choices"][idx]

    correct_answer = q_dict["answer"].strip().lower()
    if user_answer is None:
        return False, False
    if user_answer.strip().lower() == correct_answer:
        print("Correct!")
        return True, True
    else:
        print(f"Incorrect. The correct answer was: {q_dict['answer']}\n")
        return False, True

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
    for i in indices:
        q_dict = questions[i]
        correct, answered = ask_question(q_dict, time_limit=15)
        if correct:
            score += 5
            correct_count += 1
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

if __name__ == "__main__":
    main()
# 3. To-Do List App (Text-Based)
# Build a to-do list manager that:
#  Allows users to add tasks with priorities (e.g., "Buy milk - high").
#  Lets them view the current list, delete tasks by number, and mark tasks as complete.
#  Keeps looping until the user types “exit”.
#  Shows a summary at the end: number of completed tasks vs pending.
#  Skills practiced: lists, string parsing, loops, input, CRUD basics


from colorama import Fore, Back, Style, init
from datetime import datetime
init(autoreset=True)
import os
import time

#clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#loding_animation
def loading_animation(duration=1.5):
    """Displays a simple loading animation."""
    print("Processing", end="")
    for _ in range(int(duration / 0.3)):
        for dot in range(1, 4):
            print("." * dot, end="\r")
            time.sleep(0.3)
            print(" " * 15, end="\r")  
    print("exit!       ")

def get_valid_date(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input == "":
            return "-"   
        try:
            
            datetime.strptime(user_input, "%Y-%m-%d")
            return user_input  
        except ValueError:
            print("❌ Invalid date format! Please use YYYY-MM-DD.")

def get_valid_time(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input == "":
            return "-"   
        try:
            datetime.strptime(user_input, "%H:%M")
            return user_input
        except ValueError:
            print("❌ Invalid time format! Please use HH:MM.")

# Colors
CYAN = Fore.CYAN + Style.BRIGHT 
YELLOW = Fore.YELLOW + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
BLUE = Fore.BLUE + Style.BRIGHT
END = Style.RESET_ALL 
HEADER_BG = "\033[48;2;1;140;136m" + Fore.WHITE + Style.BRIGHT
OPTION_BG = "\033[48;2;147;184;183m" + Fore.BLACK + Style.NORMAL
FOOTER_BG = "\033[48;2;1;140;136m" + Fore.WHITE + Style.BRIGHT

def print_menu():
    clear_screen()
    # Header
    print(HEADER_BG + " " * 40)
    print(HEADER_BG + "        TASK MANAGER MENU               ")
    print(HEADER_BG + " " * 40 + Style.RESET_ALL)
    
    # Options
    menu_options = [
        "1. Add Task",
        "2. View Tasks",
        "3. Edit Task",
        "4. Delete Task",
        "5. mark task completed",
        "6. Summary",
        "7. Exit"
    ]
    
    for option in menu_options:
        print(OPTION_BG + f"  {option:<35}   ")
    
    # Footer
    print(FOOTER_BG + " " * 40 + Style.RESET_ALL)
# add new task
def add_task(tasks):
    print( " Type " + HEADER_BG+ "'exit'" + END+ " when you are finished.\n" )
    
    while True:
        task_name = input(OPTION_BG + " Enter your task: " + END).strip().lower()
        if task_name == "exit":
            print(HEADER_BG + " ✅Finished adding tasks!" + END)
            break
        if task_name in tasks:
            print(RED + " Task already exists! Try another one.\n" + END)
            continue
        if task_name == "":
            print(RED + " please enter your task name\n" + END)
            continue
        #priority choose
        while True:
            priority = input(f"Choose priority for '{task_name}' [{CYAN}low{END}, {CYAN}medium{END}, {CYAN}high{END}]: ").strip().lower()
            if priority not in ('low', 'medium', 'high'):
                print(RED + "❌Invalid priority. Please enter again.\n" + END)
                continue
            break
        #due date/time
        while True:
            due_date = get_valid_date(f"Enter due date"+CYAN+"(YYYY-MM-DD)"+END+ "or press Enter to skip: ").strip()
            if due_date == "":
                due_date = "-"
            due_time = get_valid_time(f"Enter due time "+CYAN+"(HH:MM) "+END+"or press Enter to skip: ").strip()
            if due_time == "":
                 due_time = "-"
            break

        
        tasks[task_name] = {
            "priority": priority,
            "due_date": due_date,
            "due_time": due_time,
            "completed": False}
        print(GREEN + f" '{task_name}'" + END + f"added with {priority} priority!\n" + END)


def print_tasks(tasks):
    # Header
    print(HEADER_BG + " " * 66)
    print(HEADER_BG + f"{'TASK MANAGER MENU':^66}")
    print(HEADER_BG + " " * 66 + Style.RESET_ALL)
    if not tasks:
        print(OPTION_BG +RED + f"{'No tasks available.':^66}")
        return
    # print(CYAN + "\n======= YOUR TASKS =======")
    print(OPTION_BG + f"{'No':>3} {'Task Name':<20}  {'Priority':^12}  {'Due Date':^14} {'Due Time':^10} ")
    print(OPTION_BG+"-"* 66)
    for i, (name, value) in enumerate(tasks.items(), start=1):
            print(OPTION_BG + f" {i}. {name:<20}  {value['priority']:^12}  {value['due_date']:^14} {value['due_time']:^10} ") 
def edit_task(tasks):
    if not tasks:
        print(RED + "No tasks available.")
        return

    print_tasks(tasks)

    task_list = list(tasks.keys())

    while True:
        choice = input("Enter task number to edit (or 'exit'): ").lower()

        if choice == "exit":
            break

        if not choice.isdigit():
            print(RED + "Enter a valid number.")
            continue

        choice = int(choice)

        if choice < 1 or choice > len(task_list):
            print(RED + "Number out of range.")
            continue

        task_name = task_list[choice - 1]
        task = tasks[task_name]

        print(GREEN + f"Editing '{task_name}'")

        # Edit name
        new_name = input(" Edit task name (press Enter to skip): ").strip().lower()
        if new_name:
            tasks[new_name] = tasks.pop(task_name)
            task_name = new_name
            task = tasks[new_name]
            "Choose priority for '{task_name}'  "
        f"Enter due date"+CYAN+"(YYYY-MM-DD)"+END+ "or press Enter to skip: "
        f"Enter due time "+CYAN+"(HH:MM) "+END+"or press Enter to skip: "

        # Edit priority
        new_priority = input(f"Edit priority [{CYAN}low{END}, {CYAN}medium{END}, {CYAN}high{END}]:(Enter to skip): ").strip().lower()
        if new_priority in ("low", "medium", "high"):
            task["priority"] = new_priority

        # Edit due date
        new_date = input("Edit due date "+CYAN+"(YYYY-MM-DD)"+END+ "or Enter to skip: ").strip()
        if new_date:
            task["due_date"] = new_date

        # Edit due time
        new_time = input("Edit due time "+CYAN+"(HH:MM) "+END+"or Enter to skip: ").strip()
        if new_time:
            task["due_time"] = new_time

        print(GREEN + "Task updated!")
        # break


def delete_task(tasks):
    # print(CYAN + "\n======= YOUR TASKS =======")
    if not tasks:
            print(RED+ "No tasks available.")
            return
    print_tasks(tasks)
    print( "type " +GREEN+"'exit'" +END+" when your done")
    task_list = list(tasks.keys())
    while True:
        
        delete_task = input("enter task number to delete: ").lower()
        if delete_task == "exit":
              break
        if not delete_task.isdigit():
            print(RED + "Enter a valid number.")
            continue
        delete_task = int(delete_task)
        if  delete_task > len(task_list):
            print(RED + "Number out of range.")
            continue
        # elif delete_task in tasks:
        #     del tasks[delete_task]
        task_name = task_list[delete_task - 1]
        del tasks[task_name]
        print(GREEN+ f"'{delete_task}' is deleted!")
        # else:
        # print(RED+ f"'{delete_task}'  not found!")
        

def mark_task_completed(tasks):
    print(CYAN + "\n======= YOUR TASKS =======")
    if not tasks:
            print(RED+ "No tasks available.")
            return
    print_tasks(tasks)
    print( "type " +GREEN+"'exit'" +END+" when your done")
    task_list = list(tasks.keys())
    while True:
        mark_task = (input("enter task number to mark complete: ")).lower()
        if mark_task == "exit":
              break
        if not mark_task.isdigit():
            print(RED + "Enter a valid number.")
            continue
        mark_task = int(mark_task)
        if mark_task < 1 or mark_task > len(task_list):
            print(RED + "Number out of range.")
            continue
        task_name = task_list[mark_task - 1]

        tasks[task_name]["completed"] = True
        print(GREEN + f"'{task_name}' marked as completed!")
        # else:
        #     print("❌task not found!")

def show_summary(tasks):
    print(CYAN+"summary:")
    completed = 0
    for t in tasks.values():
        if t["completed"]:
            completed += 1   
    pending = len(tasks) - completed
    print(GREEN+ f"Completed tasks: {completed}")
    print(YELLOW+ f"Pending tasks: {pending}")   

def main():
    tasks = {}
    print(CYAN+ "Welcome to your To-Do List!")
    while True:
        print_menu()
        x = True
        while x:
            try:
                command = int(input("Enter the number to proceed: "))
                if command <= 0:
                    print("number must be greater than 0.")
                    continue
                else:
                    x = False
            except ValueError:
                print(RED+ "❌Invalid input, please enter a number.")
                continue
            
        if command == 1:
            loading_animation(0.5)
            clear_screen()
            add_task(tasks)
        elif command == 2:
            loading_animation(0.5)
            clear_screen()
            print_tasks(tasks)
        elif command == 3:
            loading_animation(0.5)
            clear_screen()
            edit_task(tasks)
        elif command == 4:
            loading_animation(0.5)
            clear_screen()
            delete_task(tasks)
        elif command == 5:
            loading_animation(0.5)
            clear_screen()
            mark_task_completed(tasks)
        elif command == 6:
            loading_animation(0.5)
            clear_screen()
            show_summary(tasks)
        elif command == 7:
            loading_animation(0.5)
            clear_screen()
            print(BLUE+"Goodbye!")
            break
        else:
            print(RED+ "❌Invalid input, try again.")

        option = input(YELLOW+ "\nPress '1' to return to menu \npress '2' to exit: ")
        loading_animation(0.5)

        if option != "1":
            print(BLUE+"Goodbye!")
            break

if __name__ == "__main__":
    main()
    

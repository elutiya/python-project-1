# 1. Vending Machine Program
# Build a program that:
# Displays a list of snacks and drinks with item numbers and prices.
# Asks the user to choose items by number in a loop.
# Keeps track of selected items and their prices.
# Ends when the user types “done”.
# Finally prints a receipt showing:
# List of selected items with prices
# Total cost
# Skills practiced: loops, input(), conditionals, lists/dictionaries, sum(), print formatting

from colorama import Fore, Style, init
import time
import sys

# Initialize colorama
init(autoreset=True)
def loading_animation(duration=1.5):
    """Displays a simple loading animation."""
    print("Processing", end="")
    for _ in range(int(duration / 0.3)):
        for dot in range(1, 4):
            print("." * dot, end="\r")
            time.sleep(0.3)
            print(" " * 15, end="\r")  # clear line
    print("Done!       ")


print(Fore.CYAN + Style.BRIGHT + "\n====== VENDING MACHINE MENU ======\n")

food = {
    1: {"item": "skittle", "price": 10},
    2: {"item": "hershey", "price": 5},
    3: {"item": "coca", "price": 7},
    4: {"item": "sprite", "price": 4},
    5: {"item": "doritos", "price": 10}
}
lists={}
total = 0
for i, item in food.items():
    print(f"{i}.  {item['item']}  ${item['price']}")
print(Fore.YELLOW + "Type 'done' when you’re done")
while True:
        user=input("Enter item number:   ").strip().lower()
        if user =='done':
          break
        
        if not user.isdigit():  # Check if input is a number
          print(Fore.RED+" Invalid input. Please enter a valid  number.")
          continue
        user = int(user)
        if user not in food:
          print("the number is not right please enter again")
          continue

        selected = food[user]["item"]
        price = food[user]["price"]
        

       
        if selected in lists:
           lists[selected]["qty"] += 1       
        else:
          lists[selected] = {"price": price, "qty": 1}
        
       
#bill
loading_animation(1)
print("\n========= RECEIPT =========")
if not lists:
    print("No items selected.")
else:
    for item, details in lists.items():
      item_total = details["price"] * details["qty"]
      total += item_total
      print(f"- {item:<15} {details["price"]}  x{details['qty']}  = {item_total:.2f}")
    print("----------------------------")
    print( f"TOTAL:               ${total:.2f}")
    print("============================")
    print("Thank you for your purchase!")
  
    


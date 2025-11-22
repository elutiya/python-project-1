# 2. Simple Grocery Cart Checkout
# Write a program that:
# Has a predefined dictionary of groceries with prices.
# Lets the user “add” items by typing their names.
# For each valid item, asks for the quantity.
# Keeps adding to the cart until the user types "checkout".
# Displays a final bill: each item, quantity, subtotal, and total.
# Skills practiced: dictionaries, loops, input(), math operations, formatting, error handling
from colorama import Fore, Back, Style, init
init(autoreset=True)
import os
import time
import datetime
import random
#clear screen
def clear_screen():
    os.system('cls')

#loding_animation
def loading_animation(duration=1.5):
    """Displays a simple loading animation."""
    print("Processing", end="")
    for _ in range(int(duration / 0.3)):
        for dot in range(1, 4):
            print("." * dot, end="\r")
            time.sleep(0.3)
            print(" " * 15, end="\r")  # clear line
    print("Done!       ")



# Colors
CYAN = Fore.CYAN + Style.BRIGHT 
YELLOW = Fore.YELLOW + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
BLUE = Fore.BLUE + Style.BRIGHT
END = Style.RESET_ALL 
HEADER_BG = "\033[48;2;1;140;136m" + Fore.WHITE + Style.BRIGHT
OPTION_BG = "\033[48;2;147;184;183m" + Fore.BLACK + Style.NORMAL
TITLE_BG= "\033[48;2;76;161;158m"+ Fore.WHITE + Style.NORMAL
FOOTER_BG = "\033[48;2;1;140;136m" + Fore.WHITE + Style.BRIGHT

total = 0
#groceries_list
groceries_lists =dict(onion = 5, tomato = 6, potato = 7, cabbage = 6, meat = 20 )
cart={}
# print(HEADER_BG+ f"Welcome to the Grocery Store!")
# print(HEADER_BG+ f"Available items and prices:\n")
print(HEADER_BG + " " * 40)
print(HEADER_BG + "        Available items and prices      ")
print(HEADER_BG + " " * 40 + Style.RESET_ALL)
    
print(OPTION_BG+ f"{'Item':^15} {'Price ($)':^24}")
print(OPTION_BG+ "-" * 40)
for item, price in groceries_lists.items():
    print(OPTION_BG+f"{item.title():^15}  {price:^23.2f}")
print()
print("Type 'checkout' when you’re done")
#accepting data from user
while True:
    items = input("enter the name of the groceries:-").lower()
    if items == "checkout":
     break
    if items not in groceries_lists:
       print("sorry that item is not in the list")
       continue
    x= True
    while x:
        try:
            qty = int(input("enter the amount "))
            if qty <= 0:
                print("Quantity must be greater than 0.")
                continue
            else:
             x = False
        except ValueError:
            print("Please enter a valid number for quantity.")
            continue


    if items in cart:
        cart[items] += qty
    else:
        cart[items] = qty
now = datetime.datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")
transaction_number = random.randint(10000, 99999)
print("\n Reciept")
print("abcd PLC")
print("-------------------------------------------------")
print("-" * 30)
for item, qty in cart.items():
    price = groceries_lists[item]   
    subtotal = price * qty
    total += subtotal
    print(f"{item.title():10} x {qty:<3} = ${subtotal:.2f}")
    # print(item, qty, "subtotal", subtotal , "total", total)
print("-" * 30)
print(f"Total: ${total:.2f}")
print("Vending Machine 001  Location: Arat Killo Plaza")
print(f"Date & Time: {date_time}")
print(f"Transaction #: {transaction_number}")
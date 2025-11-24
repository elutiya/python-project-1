# 2. Simple Grocery Cart Checkout
# Write a program that:
# Has a predefined dictionary of groceries with prices.
# Lets the user “add” items by typing their names.
# For each valid item, asks for the quantity.
# Keeps adding to the cart until the user types "checkout".
# Displays a final bill: each item, quantity, subtotal, and total.
# Skills practiced: dictionaries, loops, input(), math operations, formatting, error handling
from colorama import Fore, Style, init
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
CYAN_GREEN = "\033[38;2;169;212;170m" + Style.BRIGHT
Black = Fore.BLACK + Style.BRIGHT 
YELLOW = Fore.YELLOW + Style.NORMAL
RED = Fore.RED + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
END = Style.RESET_ALL 
HEADER_BG = "\033[48;2;139;195;74m" + Fore.WHITE + Style.BRIGHT
OPTION_BG = "\033[48;2;169;212;170m"+ Fore.BLACK + Style.BRIGHT
WHITE_BG = "\033[48;2;255;255;255m"

total = 0
#groceries_list
groceries_lists =dict(onion = 5, tomato = 6, potato = 7, cabbage = 6, meat = 20 )
cart={}
#menu
print(HEADER_BG + " " * 39)
print(HEADER_BG + "        Available items and prices     ")
print(HEADER_BG + " " * 39 + Style.RESET_ALL)  


print(OPTION_BG+ Black+ f"{'Item(K.G)':^15} {'Price ($)':^23}")
print(OPTION_BG+ "-" * 39)

for item, price in groceries_lists.items():
    print(OPTION_BG+ Black+ f"{item.title():^15}  {price:^22.2f}")
print()
print(f"Type" +GREEN+"'checkout'"+END+" when you’re done")
#accepting data from user
while True:
    items = input(CYAN_GREEN+ "enter the name of the groceries:-"+END).lower()
    if items == "checkout":
     if not cart:
         print(YELLOW+"🃏 The cart is empty please add groceries")
         continue
     else:
         break
    if items not in groceries_lists:
       print(RED+f" ❌ '{ items}' is not in the list")
       continue
    #accepting qty
    x= True
    while x:
        try:
            qty = int(input(CYAN_GREEN+ "enter how many K.G you want "+END))
            if qty <= 0:
                print(YELLOW+"⚠️  Quantity must be greater than 0.")
                continue
            else:
             print(GREEN+ f"✅ '{items}'"+END+  " is added to your cart")
             x = False
        except ValueError:
            print(YELLOW+"⚠️  Please enter a valid quantity.")
            continue
    if items in cart:
        cart[items] += qty
    else:
        cart[items] = qty
now = datetime.datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")
transaction_number = random.randint(10000, 99999)
#reciept_print
loading_animation(0.5)
clear_screen() #clear previous screen
print(WHITE_BG+ f"{'=' * 50}")
print(WHITE_BG+f"{'GROCERY RECEIPT':^50}")
print(WHITE_BG+ f"{'=' * 50}")

print(WHITE_BG+ f" {'Store:    ABCD PLC':<49}")
print(WHITE_BG+ f" {'Location: Arat Killo Plaza':<49}")
print(WHITE_BG+ f" {'Machine:  VM-001':<49}")
print(WHITE_BG+"-" * 50)

print(WHITE_BG+f" Transaction #: {transaction_number:<34}")
print(WHITE_BG+f" Date & Time:   {date_time:<34}")
print(WHITE_BG+"-" * 50)

print(WHITE_BG+f" {'Item(K.G)':<15}{'Price':^10}{'Qty':^10}{'Subtotal':^14}")
print(WHITE_BG+"-" * 50)

for item, qty in cart.items():
    price = groceries_lists[item]   
    subtotal = price * qty
    total += subtotal
    print(WHITE_BG+f" {item.title():<15} ${price:<9.2f} x {qty:<8} = ${subtotal:<7.2f} ")
    print(WHITE_BG+"-" * 50)
#total  
print(WHITE_BG+f" Total: {'$':>34}{total :<7.2f} ")
print(WHITE_BG+"-" * 50)
print(WHITE_BG+f"{'Thank you for shopping!':^50}")
print(WHITE_BG+"-" * 50)

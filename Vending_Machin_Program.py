import datetime
import time

# 🎨 Colors & Styles
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"


def loading_animation(duration=1.5):
    """Displays a simple loading animation with colors."""
    print(CYAN + "Processing" + RESET, end="")
    for _ in range(int(duration / 0.3)):
        for dot in range(1, 4):
            print(YELLOW + "." * dot + RESET, end="\r")
            time.sleep(0.3)
            print(" " * 15, end="\r")
    print(GREEN + "Done!" + RESET)


# 🛒 Menu
menu = {
    1: ["🍟 Chips", 10],
    2: ["🥤 Soda", 25],
    3: ["🍫 Chocolate Bar", 15],
    4: ["💧 Water Bottle", 12.20],
    5: ["🍪 Cookies", 13.07],
    6: ["🧃 Juice Box", 12.50],
    7: ["🍭 Candy", 2.30],
    8: ["🍬 Gum", 1]
}

transaction_counter = 1  # 🔢 Keeps track of transactions

while True:
    selected_items = {}

    print(GREEN + BOLD + "✨=== Welcome to the Arat Kilo Vending Machine ===✨" + RESET)
    print(BG_BLUE + " " * 33)
    print(BG_BLUE + BOLD + f"📋 {'Menu':<17}   {' price':10}" + RESET)
    print(BG_BLUE + " " * 33)

    for number, (item, price) in menu.items():
        print(BG_YELLOW + BOLD + f"{number}. {item:<17} - ${price:<8.2f}" + RESET)

    while True:
        choice = input(GREEN + BOLD +
                       "\nEnter item number (or 'edit' to modify cart, 'done' to finish): "
                       + RESET).strip().lower()

        if choice == "done":
            if not selected_items:
                print(RED + BOLD +
                      "⚠️ Your cart is empty. Please add at least one item before finishing." + RESET)
                continue
            break

        if choice == "edit":
            if not selected_items:
                print(RED + BOLD + "⚠️ Your cart is empty. Nothing to edit." + RESET)
                continue

            print(YELLOW + BOLD + "\n🛒 Current Cart:" + RESET)
            for num, qty in selected_items.items():
                item, price = menu[num]
                print(f"{num}. {item} - Qty: {qty}")

            edit_choice = input(CYAN + BOLD +
                                "Enter item number to update/remove (or 'back' to return): " +
                                RESET).strip().lower()

            if edit_choice == "back":
                continue

            if not edit_choice.isdigit() or int(edit_choice) not in selected_items:
                print(RED + BOLD + "❌Invalid choice! Please select an item in your cart." + RESET)
                continue

            edit_choice = int(edit_choice)
            print(CYAN + "What would you like to do?" + RESET)
            print("1. Update quantity")
            print("2. Remove item")

            action = input("Enter 1 or 2: ").strip()

            if action == "2":  # Remove
                del selected_items[edit_choice]
                print(YELLOW + f"🗑️ Removed {menu[edit_choice][0]} from your cart." + RESET)

            elif action == "1":  # Update
                while True:
                    new_qty = input(CYAN + f"Enter new quantity for {menu[edit_choice][0]}: " + RESET).strip()
                    if new_qty.isdigit() and int(new_qty) > 0:
                        selected_items[edit_choice] = int(new_qty)
                        print(GREEN + f"✅ Updated {menu[edit_choice][0]} to {new_qty}." + RESET)
                        break
                    else:
                        print(RED + "❌ Invalid quantity. Please enter a positive number." + RESET)
            else:
                print(RED + "❌ Invalid choice. Please enter 1 or 2." + RESET)
            continue

        if not choice.isdigit() or int(choice) not in menu:
            print(RED + BOLD + "❌Invalid input! Please enter a valid input." + RESET)
            continue

        choice = int(choice)
        while True:
            quantity = input(GREEN + BOLD +
                             f"How many {menu[choice][0]} would you like? " + RESET).strip()
            if not quantity.isdigit() or int(quantity) <= 0:
                print(RED + BOLD + "❌Invalid quantity please enter a valid input!." + RESET)
                continue
            quantity = int(quantity)
            break

        selected_items[choice] = selected_items.get(choice, 0) + quantity
        print(GREEN + BOLD + f"🛒 Added {quantity} x {menu[choice][0]} to your cart." + RESET)

    # 🧾 Receipt
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    today = now.strftime("%Y%m%d")
    transaction_number = f"TR-{today}-{transaction_counter:03d}"
    transaction_counter += 1

    loading_animation(0.3)
    print(BG_WHITE + YELLOW + BOLD + "\n🧾 ======================= Receipt =======================🧾")
    print(BG_WHITE + CYAN + f"{'ABCD PLC':<60}")
    print(BG_WHITE + CYAN + "Vending Machine 001  Location: Arat Killo Plaza")
    print(BG_WHITE + CYAN + f"Date & Time: {date_time}")
    print(BG_WHITE + CYAN + f"Transaction #: {transaction_number}")
    print(BG_WHITE + CYAN + "-------------------------------------------------")
    print(BG_WHITE + CYAN + BOLD + f"{'Item':<15}{'Qty':<10}{'Price':<10}{'Line Total'}")
    print(BG_WHITE + CYAN + "-------------------------------------------------" + RESET)

    total = 0
    for number, quantity in selected_items.items():
        item, price = menu[number]
        line_total = price * quantity
        print(BG_WHITE + CYAN + f"{item:<15}{quantity:<10}${price:<9.2f}${line_total:.2f}" + RESET)
        total += line_total

    print(BG_WHITE + CYAN + "-------------------------------------------------" + RESET)
    print(BG_WHITE + CYAN + BOLD + f"{'TOTAL':<15}{'':<10}{'':<10}${total:.2f}" + RESET)
    print(BG_WHITE + CYAN + "=================================================" + RESET)

    # 💳 Payment
    while True:
        try:
            payment = float(input(GREEN + BOLD +
                                  f"Please insert payment (Total:${total:.2f}): " + RESET))
            if payment < total:
                print(RED + f"⚠️ Insufficient payment! You still owe ${total - payment:.2f}." + RESET)
            else:
                loading_animation(0.5)
                change = payment - total
                print(GREEN + BOLD +
                      f"✅ Payment accepted! Your change is ${change:.2f}" + RESET)
                break
        except ValueError:
            print(RED + "❌ Invalid input! Please enter a valid amount." + RESET)

    print(BG_YELLOW + BOLD +
          "🎉🎉 Thank you for shopping at Arat Kilo Vending Machine! 🎉🎉" + RESET)

    again = input(GREEN + "\nWould you like to make another purchase? (yes/no): " +
                  RESET).strip().lower()
    if again != "yes":
        print(BG_YELLOW + CYAN + BOLD +
              "👋 Thank you for using Arat Kilo Vending Machine! Goodbye!" + RESET)
        
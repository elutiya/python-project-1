# 4. Movie Ticket Booking Simulation
# Simulate a movie theater booking system that:

#     Shows a list of available movie titles, showtimes, and seat prices.
#     Asks the user to choose a movie and number of tickets.
#     Confirms total price and asks if they want to book another movie.
#     Ends when they say “no” and displays total bookings and cost.
# > Skills practiced: loops, input, conditionals, calculations, nested dictionaries

from __future__ import annotations
import datetime
import time
from typing import Dict, List, Tuple

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

END = RESET
HEADER_BG = BG_CYAN
OPTION_BG = BG_YELLOW
FOOTER_BG = BG_CYAN


def loading_animation(duration=1.5):
    """Displays a simple loading animation."""
    print(CYAN + "Processing" + END, end="")
    for _ in range(int(duration / 0.3)):
        for dot in range(1, 4):
            print("." * dot, end="\r")
            time.sleep(0.3)
            print(" " * 15, end="\r")
    print(GREEN + "Done!" + END)



def _make_seats(rows: str = "ABCD", per_row: int = 10) -> List[str]:
    return [f"{row}{num}" for row in rows for num in range(1, per_row + 1)]


def _int_input(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                print(GREEN + f"Please enter a number >= {min_val}." + END)
                continue
            if max_val is not None and val > max_val:
                print(GREEN + f"Please enter a number <= {max_val}." + END)
                continue
            return val
        except ValueError:
            print(RED + "Invalid integer — please try again." + END)


def _float_input(prompt: str, min_val: float | None = None) -> float:
    while True:
        try:
            val = float(input(prompt))
            if min_val is not None and val < min_val:
                print(GREEN + f"Please enter an amount >= {min_val}." + END)
                continue
            return val
        except ValueError:
            print(RED + "Invalid number — please try again." + END)


def _choice_input(prompt: str, options: List[str]) -> str:
    opts = [o.lower() for o in options]
    while True:
        val = input(prompt).strip().lower()
        if val in opts:
            return options[opts.index(val)]
    print(GREEN + f"Please choose one of: {', '.join(options)}" + END)


def pretty_receipt(
    booking_ref: str,
    transaction: int,
    recipient: int,
    booking_time: str,
    movie: str,
    showtime: str,
    tickets: int,
    seat_type: str,
    seats: List[str],
    unit_price: float,
    extra_cost: float,
    total: float,
) -> str:
    lines = []
    lines.append(BG_WHITE + f"{'='*54:<54}" + END)
    lines.append(BG_WHITE + f"{' 🧾 MOVIE BOOKING RECEIPT':^53}" + END)
    lines.append(BG_WHITE + f"{'='*54:<54}" + END)
    lines.append(BG_WHITE + f"{('Booking Ref:   ' + str(booking_ref)):<54}" + END)
    lines.append(BG_WHITE + f"{('Transaction #: ' + str(transaction)):<54}" + END)
    lines.append(BG_WHITE + f"{('Recipient #:   ' + str(recipient)):<54}" + END)
    lines.append(BG_WHITE + f"{('Date/Time:     ' + str(booking_time)):<54}" + END)
    lines.append(BG_WHITE + f"{'-'*54:<54}" + END)
    lines.append(BG_WHITE + f"{('Movie:         ' + str(movie)):<54}" + END)
    lines.append(BG_WHITE + f"{('Showtime:      ' + str(showtime)):<54}" + END)
    lines.append(BG_WHITE + f"{('Tickets:       ' + str(tickets)):<54}" + END)
    lines.append(BG_WHITE + f"{('Seat Type:     ' + str(seat_type)):<54}" + END)
    seats_str = ', '.join(seats)
    lines.append(BG_WHITE + f"{('Seats:         ' + seats_str):<54}" + END)
    lines.append(BG_WHITE + f"{('Price:         ' + f'${unit_price:.2f} each (+${extra_cost} {seat_type})'):<54}" + END)
    lines.append(BG_WHITE + f"{('Total:         ' + f'${total:.2f}'):<54}" + END)
    lines.append(BG_WHITE + f"{'='*54:<54}" + END)
    return "\n".join(lines)

def movie_booking_system():
    movies: Dict[str, Dict[str, object]] = {
        "Avengers: Endgame": {"showtime": "6:00 PM", "price": 12},
        "Inception": {"showtime": "8:00 PM", "price": 10},
        "Interstellar": {"showtime": "9:00 PM", "price": 15},
        "The Dark Knight": {"showtime": "7:30 PM", "price": 11},
    }

    seat_types = {"Regular": 0, "VIP": 5}

    seat_template = _make_seats(rows="ABCD", per_row=10)
    vip_count = 10
    vip_template = seat_template[-vip_count:]
    regular_template = seat_template[:-vip_count]
    seat_map: Dict[str, Dict[str, List[str]]] = {
        title: {"Regular": regular_template.copy(), "VIP": vip_template.copy()} for title in movies
    }

    total_bookings: List[Tuple[int, str, float, int, str, str, str, List[str]]] = []
    total_cost = 0.0
    recipient_counter = 1000
    transaction_counter = 1
    print('\n')
    print(HEADER_BG + CYAN + f"{'🎬 Welcome to the Movie Theater Booking System!':^54}" + END)

    try:
        while True:
            print(BG_WHITE + CYAN + f"{'🎬 Available Movies':^54}" + END)
            print(OPTION_BG + f"{'No.':<5}{'Title':<25}{'Showtime':<15}{'Price ($)':<10}" + END)
            print(OPTION_BG + "-" * 55 + END)
            for i, (title, details) in enumerate(movies.items(), start=1):
                print(OPTION_BG + CYAN + f"{i:<5}{title:<25}{details['showtime']:<15}{details['price']:<10}" + END)

            choice = _int_input(GREEN + "\nEnter the number of the movie you want to book: " + END, 1, len(movies))
            selected_movie = list(movies.keys())[choice - 1]
            ticket_price = float(movies[selected_movie]["price"])

            available = len(seat_map[selected_movie]["Regular"]) + len(seat_map[selected_movie]["VIP"])
            print(GREEN + f"Seats available for '{selected_movie}': {available} (Regular: {len(seat_map[selected_movie]['Regular'])}, VIP: {len(seat_map[selected_movie]['VIP'])})" + END)
            tickets = _int_input(GREEN + f"🎟️ How many tickets for '{selected_movie}'? " + END, 1, available)

            seat_choice = _choice_input(GREEN + "Choose seat type (Regular/VIP): " + END, list(seat_types.keys()))
            extra_cost = seat_types[seat_choice]

            cost = tickets * (ticket_price + extra_cost)

            booking_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            recipient_number = recipient_counter

            recipient_counter += 1

            today_str = datetime.datetime.now().strftime("%Y%m%d")
            booking_ref = f"BK-{today_str}-{transaction_counter:03d}"

            if tickets > len(seat_map[selected_movie][seat_choice]):
                print(RED + f"⚠️ Not enough {seat_choice} seats available. Available: {len(seat_map[selected_movie][seat_choice])}" + END)
                continue

            assigned_raw = seat_map[selected_movie][seat_choice][:tickets]
            seat_map[selected_movie][seat_choice] = seat_map[selected_movie][seat_choice][tickets:]

            print(pretty_receipt(
                booking_ref=booking_ref,
                transaction=transaction_counter,
                recipient=recipient_number,
                booking_time=booking_time,
                movie=selected_movie,
                showtime=movies[selected_movie]["showtime"],
                tickets=tickets,
                seat_type=seat_choice,
                seats=assigned_raw,
                unit_price=ticket_price,
                extra_cost=extra_cost,
                total=cost,
            ))


            total_bookings.append((
                tickets,
                selected_movie,
                cost,
                recipient_number,
                booking_time,
                seat_choice,
                booking_ref,
                assigned_raw,
            ))
            total_cost += cost
            transaction_counter += 1

            another = _choice_input(GREEN + "Do you want to book another movie? (yes/no): " + END, ["yes", "no"])
            if another.lower() == "no":
                break

        print(BG_WHITE + CYAN + f"{'📊 Booking Summary':^119}" + END)
        header = f"{'Qty':<5}{'Film Title':<25}{'Price':<10}{'Recipient':<12}{'SeatType':<10}{'Booking Ref':<20}{'Date/Time':<25}{'Seats'}"
        print(OPTION_BG + f"{header:<120}" + END)
        print(OPTION_BG + "-" * 120 + END)
        for qty, movie, cost, recipient, time, seat_type, ref, seats in total_bookings:
            seats_str = ", ".join(seats)
            row = f"{qty:<5}{movie:<25}${cost:<9.2f}{recipient:<12}{seat_type:<10}{ref:<20}{time:<25}{seats_str}"
            print(OPTION_BG + f"{row:<120}" + END)
        print(OPTION_BG + "-" * 120 + END)
        print(GREEN + f"\n💰 Grand Total: ${total_cost:.2f}" + END)

        while True:
            payment = _float_input(GREEN + f"💳 Please insert payment (Total: ${total_cost:.2f}): " + END, min_val=0.0)
            if payment < total_cost:
                loading_animation(0.5)
                print(RED + f"⚠️ Insufficient payment! You still owe ${total_cost - payment:.2f}." + END)
            else:
                change = payment - total_cost
                print(GREEN + f"✅ Payment accepted! Your change is ${change:.2f}" + END)
                break

        print(HEADER_BG + CYAN + "🎉 Thank you for booking with us!" + END)

    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting booking system. Goodbye." + END)
        return

movie_booking_system()
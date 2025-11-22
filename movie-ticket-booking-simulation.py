"""Movie Theater Booking System with seat allocation per movie/showtime.

This variant keeps bookings in memory only (no disk persistence). It:
- Tracks seat availability per film instead of globally.
- Adds safe input helpers and validation.
- Keeps bookings in-memory for the current run.
- Guards execution behind `if __name__ == '__main__'` so the module can be imported
    without side effects (easier testing).
"""

from __future__ import annotations

import datetime
from typing import Dict, List, Tuple


def _make_seats(rows: str = "ABCD", per_row: int = 10) -> List[str]:
    return [f"{row}{num}" for row in rows for num in range(1, per_row + 1)]


def _int_input(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Please enter a number >= {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Please enter a number <= {max_val}.")
                continue
            return val
        except ValueError:
            print("Invalid integer — please try again.")


def _float_input(prompt: str, min_val: float | None = None) -> float:
    while True:
        try:
            val = float(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Please enter an amount >= {min_val}.")
                continue
            return val
        except ValueError:
            print("Invalid number — please try again.")


def _choice_input(prompt: str, options: List[str]) -> str:
    opts = [o.lower() for o in options]
    while True:
        val = input(prompt).strip().lower()
        if val in opts:
            return options[opts.index(val)]
        print(f"Please choose one of: {', '.join(options)}")


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
    lines.append("\n" + "=" * 40)
    lines.append(" 🧾 MOVIE BOOKING RECEIPT")
    lines.append("=" * 40)
    lines.append(f"Booking Ref:   {booking_ref}")
    lines.append(f"Transaction #: {transaction}")
    lines.append(f"Recipient #:   {recipient}")
    lines.append(f"Date/Time:     {booking_time}")
    lines.append("-" * 40)
    lines.append(f"Movie:         {movie}")
    lines.append(f"Showtime:      {showtime}")
    lines.append(f"Tickets:       {tickets}")
    lines.append(f"Seat Type:     {seat_type}")
    lines.append(f"Seats:         {', '.join(seats)}")
    lines.append(f"Price:         ${unit_price:.2f} each (+${extra_cost} {seat_type})")
    lines.append(f"Total:         ${total:.2f}")
    lines.append("=" * 40 + "\n")
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

    print("🎬 Welcome to the Movie Theater Booking System!\n")

    try:
        while True:
            print("Available Movies:")
            for i, (title, details) in enumerate(movies.items(), start=1):
                print(f"{i}. {title} - Showtime: {details['showtime']} - Price: ${details['price']}")

            choice = _int_input("\nEnter the number of the movie you want to book: ", 1, len(movies))
            selected_movie = list(movies.keys())[choice - 1]
            ticket_price = float(movies[selected_movie]["price"])

            available = len(seat_map[selected_movie]["Regular"]) + len(seat_map[selected_movie]["VIP"])
            print(f"Seats available for '{selected_movie}': {available} (Regular: {len(seat_map[selected_movie]['Regular'])}, VIP: {len(seat_map[selected_movie]['VIP'])})")
            tickets = _int_input(f"🎟️ How many tickets for '{selected_movie}'? ", 1, available)

            seat_choice = _choice_input("Choose seat type (Regular/VIP): ", list(seat_types.keys()))
            extra_cost = seat_types[seat_choice]

            cost = tickets * (ticket_price + extra_cost)

            booking_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            recipient_number = recipient_counter

            recipient_counter += 1

            today_str = datetime.datetime.now().strftime("%Y%m%d")
            booking_ref = f"BK-{today_str}-{transaction_counter:03d}"

            if tickets > len(seat_map[selected_movie][seat_choice]):
                print(f"⚠️ Not enough {seat_choice} seats available. Available: {len(seat_map[selected_movie][seat_choice])}")
                continue

            assigned_raw = seat_map[selected_movie][seat_choice][:tickets]
            seat_map[selected_movie][seat_choice] = seat_map[selected_movie][seat_choice][tickets:]
            assigned_tagged = [f"{s} ({seat_choice})" for s in assigned_raw]

            print(pretty_receipt(
                booking_ref=booking_ref,
                transaction=transaction_counter,
                recipient=recipient_number,
                booking_time=booking_time,
                movie=selected_movie,
                showtime=movies[selected_movie]["showtime"],
                tickets=tickets,
                seat_type=seat_choice,
                seats=assigned_tagged,
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

            another = _choice_input("Do you want to book another movie? (yes/no): ", ["yes", "no"])
            if another.lower() == "no":
                break

        print("\n📊 Booking Summary:")
        print(f"{'Qty':<5}{'Film Title':<25}{'Price':<10}{'Recipient':<12}{'SeatType':<10}{'Booking Ref':<20}{'Date/Time':<25}{'Seats'}")
        print("-" * 120)
        for qty, movie, cost, recipient, time, seat_type, ref, seats in total_bookings:
            seats_str = ", ".join(seats)
            print(
                f"{qty:<5}{movie:<25}${cost:<9.2f}{recipient:<12}{seat_type:<10}{ref:<20}{time:<25}{seats_str}"
            )
        print("-" * 120)
        print(f"\n💰 Grand Total: ${total_cost:.2f}")

        while True:
            payment = _float_input(f"💳 Please insert payment (Total: ${total_cost:.2f}): ", min_val=0.0)
            if payment < total_cost:
                print(f"⚠️ Insufficient payment! You still owe ${total_cost - payment:.2f}.")
            else:
                change = payment - total_cost
                print(f"✅ Payment accepted! Your change is ${change:.2f}")
                break

        print("🎉 Thank you for booking with us!")

    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting booking system. Goodbye.")


if __name__ == "__main__":
    # Run the system
    movie_booking_system()
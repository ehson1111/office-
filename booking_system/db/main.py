import sqlite3
from datetime import datetime, timedelta
import argparse
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'database.db')

def connect_db():
    return sqlite3.connect(DB_PATH)

def check_availability(room, date, time):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT user_name, time FROM bookings
        WHERE room_number = ? AND date = ? AND time = ?
    ''', (room, date, time))

    booking = cursor.fetchone()
    conn.close()

    if booking:
        print(f"Кабинет {room} занят {booking[0]} до {booking[1]}")
    else:
        print(f"Кабинет {room} свободен в {date} {time}")

def book_room(room, date, time, user_name, email, phone):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM bookings WHERE room_number = ? AND date = ? AND time = ?
    ''', (room, date, time))

    if cursor.fetchone():
        print(f"Кабинет {room} уже занят на {date} {time}")
        conn.close()
        return

    cursor.execute('''
        INSERT INTO bookings (room_number, date, time, user_name, email, phone)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (room, date, time, user_name, email, phone))

    conn.commit()
    conn.close()

    notify_user(email, phone, room, date, time)

def notify_user(email, phone, room, date, time):
    print(f"[EMAIL to {email}]\nВаш кабинет №{room} забронирован на {date} в {time}\n")
    print(f"[SMS to {phone}]\nКабинет №{room}, дата: {date}, время: {time}\n")

def main():
    parser = argparse.ArgumentParser(description="Office Booking CLI")
    subparsers = parser.add_subparsers(dest="command")

    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("--room", type=int, required=True)
    check_parser.add_argument("--date", required=True)
    check_parser.add_argument("--time", required=True)

    book_parser = subparsers.add_parser("book")
    book_parser.add_argument("--room", type=int, required=True)
    book_parser.add_argument("--date", required=True)
    book_parser.add_argument("--time", required=True)
    book_parser.add_argument("--user", required=True)
    book_parser.add_argument("--email", required=True)
    book_parser.add_argument("--phone", required=True)

    args = parser.parse_args()

    if args.command == "check":
        check_availability(args.room, args.date, args.time)
    elif args.command == "book":
        book_room(args.room, args.date, args.time, args.user, args.email, args.phone)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

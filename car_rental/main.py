"""Konsol menyusi: python main.py"""
from datetime import date

import reports
from db import get_db
from errors import AppError
from models import cars, customers
from services import payment, rental, repair, warehouse


def ask(text):
    return input(f"{text}: ").strip()


def number(text):
    try:
        return int(ask(text))
    except ValueError:
        raise AppError("Butun son kiriting")


def day(text):
    value = ask(f"{text} (YYYY-MM-DD, bo'sh = bugun)")
    try:
        return date.fromisoformat(value) if value else date.today()
    except ValueError:
        raise AppError("Sana noto'g'ri")


def choose(items, label):
    items = list(items)
    if not items:
        raise AppError("Ro'yxat bo'sh")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {label(item)}")
    i = number("Tanlang")
    if not 1 <= i <= len(items):
        raise AppError("Bunday raqam yo'q")
    return items[i - 1]


def car_label(c):
    return f"{c['brand']} {c['model']} {c['plate_number']} [{c['status']}] {c['daily_price']} so'm"


def customer_label(c):
    return f"{c['full_name']} {c['phone']}"


def pick_car(db, status=None):
    return choose(cars.all_cars(db, status), car_label)["_id"]


def pick_customer(db):
    return choose(customers.search(db, ask("Qidiruv (bo'sh = hammasi)")), customer_label)["_id"]


def pick_rental(db, query):
    def label(r):
        car = db.cars.find_one({"_id": r["car_id"]})
        who = db.customers.find_one({"_id": r["customer_id"]})
        return f"{car['plate_number']} {who['full_name']} {r['start_date']}..{r['end_date']} {r['total']}"
    return choose(db.rentals.find(query), label)["_id"]


def pick_repair(db, status):
    def label(r):
        return f"{db.cars.find_one({'_id': r['car_id']})['plate_number']} {r['work']} {r['cost']}"
    return choose(db.repairs.find({"status": status}), label)["_id"]


def pick_part(db):
    return choose(db.parts.find({}), lambda p: f"{p['name']} ({p['maker']}) qoldiq: {p['stock']}")["_id"]


def add_car(db):
    cars.add(db, ask("Marka"), ask("Model"), number("Yil"), ask("Davlat raqami"),
             number("Kunlik narx"), number("Probeg"))


def list_cars(db):
    for c in cars.all_cars(db):
        print(car_label(c), f"probeg: {c['mileage']}")


def change_price(db):
    cars.set_price(db, pick_car(db), number("Yangi kunlik narx"))


def add_customer(db):
    customers.add(db, ask("F.I.Sh."), ask("Telefon"), ask("Pasport"),
                  ask("Guvohnoma"), ask("Manzil"))


def customer_history(db):
    for r in customers.history(db, pick_customer(db)):
        print(r["start_date"], r["end_date"], r["total"], r["status"])


def open_rental(db):
    rid = rental.open_rental(db, pick_car(db, "free"), pick_customer(db),
                             day("Boshlanish"), day("Tugash"))
    print("Jami summa:", db.rentals.find_one({"_id": rid})["total"])


def extend_rental(db):
    print("Yangi summa:", rental.extend(db, pick_rental(db, {"status": "active"}), day("Yangi tugash")))


def close_rental(db):
    rid = pick_rental(db, {"status": "active"})
    order = rental.close(db, rid, day("Qaytarish"), number("Probeg"),
                         ask("Shikast (yo'q bo'lsa bo'sh)"))
    print("Jami summa:", db.rentals.find_one({"_id": rid})["total"])
    if order:
        print("Ta'mirlash buyurtmasi ochildi")


def open_repair(db):
    repair.open_repair(db, pick_car(db, "free"), ask("Ish turi"))


def use_part(db):
    repair.use_part(db, pick_repair(db, "open"), pick_part(db), number("Miqdor"))


def close_repair(db):
    print("Ish narxi:", repair.close(db, pick_repair(db, "open"), number("Xizmat haqi")))


def add_part(db):
    warehouse.add_part(db, ask("Nomi"), ask("Ishlab chiqaruvchi"), number("Narx"),
                       number("Eng kam qoldiq"), number("Almashtirish, km (0 = yo'q)"),
                       number("Almashtirish, oy (0 = yo'q)"))


def receive_part(db):
    warehouse.receive(db, pick_part(db), number("Miqdor"))


def pay_rental(db):
    rid = pick_rental(db, {})
    payment.pay(db, number("Summa"), ask("Turi (naqd/karta)"), rental_id=rid)


def pay_repair(db):
    rid = pick_repair(db, "done")
    payment.pay(db, number("Summa"), ask("Turi (naqd/karta)"), repair_id=rid)


def show_reports(db):
    today = date.today()
    income, expense = reports.monthly(db, today.year, today.month)
    print(f"Shu oy: tushum {income}, xarajat {expense}")
    print("Eng ko'p ijaraga olinganlar:")
    for car, n in reports.top_cars(db):
        print(" ", car["plate_number"], n)
    print("Kam qolgan qismlar:")
    for p in warehouse.low_stock(db):
        print(" ", p["name"], p["stock"])
    print("Qarzdorlar:")
    for who, debt in reports.debtors(db):
        print(" ", customer_label(who), debt)
    print("Texnik xizmat muddati yaqin:")
    for car, part in repair.maintenance_due(db):
        print(" ", car["plate_number"], part["name"])


MENU = [
    ("Avtomobil qo'shish", add_car), ("Avtomobillar ro'yxati", list_cars),
    ("Kunlik narxni o'zgartirish", change_price),
    ("Mijoz qo'shish", add_customer), ("Mijoz ijara tarixi", customer_history),
    ("Ijara ochish", open_rental), ("Ijarani uzaytirish", extend_rental),
    ("Avtomobilni qaytarib olish", close_rental),
    ("Ta'mir ochish", open_repair), ("Ta'mirga qism ishlatish", use_part),
    ("Ta'mirni yopish", close_repair),
    ("Yangi ehtiyot qism", add_part), ("Qism kirimi", receive_part),
    ("Ijara to'lovi", pay_rental), ("Ta'mir to'lovi", pay_repair),
    ("Hisobotlar", show_reports),
]


def main():
    try:
        db = get_db()
    except Exception as error:
        raise SystemExit(f"MongoDB'ga ulanib bo'lmadi: {error}")
    while True:
        print("\n=== Avtomobil ijarasi ===")
        for i, (title, _) in enumerate(MENU, 1):
            print(f"{i}. {title}")
        print("0. Chiqish")
        try:
            choice = number("Tanlang")
            if choice == 0:
                return
            if not 1 <= choice <= len(MENU):
                raise AppError("Bunday bo'lim yo'q")
            MENU[choice - 1][1](db)
        except AppError as error:
            print("Xato:", error)
        except (KeyboardInterrupt, EOFError):
            return


if __name__ == "__main__":
    main()

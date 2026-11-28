"""Ijara: ochish, uzaytirish, yopish. Sanalar datetime.date ko'rinishida."""
from datetime import date

from errors import AppError
from models import cars
from models.common import get, now
from services import repair


def _days(start, end):
    days = (end - start).days
    if days < 1:
        raise AppError("Tugash sanasi boshlanishdan keyin bo'lishi kerak")
    return days


def open_rental(db, car_id, customer_id, start, end):
    get(db.customers, customer_id, "Mijoz")
    car = get(db.cars, car_id, "Avtomobil")
    days = _days(start, end)
    cars.take(db, car_id, "rented")
    return db.rentals.insert_one({
        "car_id": car_id,
        "customer_id": customer_id,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "daily_price": car["daily_price"],
        "total": days * car["daily_price"],
        "status": "active",
        "created_at": now(),
    }).inserted_id


def _active(db, rental_id):
    doc = get(db.rentals, rental_id, "Ijara")
    if doc["status"] != "active":
        raise AppError("Ijara allaqachon yopilgan")
    return doc


def extend(db, rental_id, new_end):
    doc = _active(db, rental_id)
    if new_end <= date.fromisoformat(doc["end_date"]):
        raise AppError("Yangi sana eskisidan keyin bo'lishi kerak")
    total = _days(date.fromisoformat(doc["start_date"]), new_end) * doc["daily_price"]
    db.rentals.update_one({"_id": rental_id},
                          {"$set": {"end_date": new_end.isoformat(), "total": total}})
    return total


def close(db, rental_id, return_date, mileage, damage=""):
    """Qaytarib olish. Kechikkan kunlar qo'shib hisoblanadi.

    Shikast bo'lsa, ta'mirlash buyurtmasi ochiladi va uning id si qaytadi.
    """
    doc = _active(db, rental_id)
    car = get(db.cars, doc["car_id"], "Avtomobil")
    start = date.fromisoformat(doc["start_date"])
    if return_date < start:
        raise AppError("Qaytarish sanasi boshlanishdan oldin")
    if mileage < car["mileage"]:
        raise AppError("Probeg avvalgidan kam bo'lishi mumkin emas")
    end = max(return_date, date.fromisoformat(doc["end_date"]))
    total = (end - start).days * doc["daily_price"]
    db.rentals.update_one({"_id": rental_id}, {"$set": {
        "status": "closed", "returned_at": return_date.isoformat(), "total": total}})
    db.cars.update_one({"_id": car["_id"]}, {"$set": {"mileage": mileage}})
    cars.release(db, car["_id"])
    if damage.strip():
        return repair.open_repair(db, car["_id"], damage, rental_id=rental_id)
    return None

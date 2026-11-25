"""Ta'mirlash buyurtmalari va texnik xizmat muddatlari."""
from datetime import date, timedelta

from errors import AppError
from models import cars
from models.common import get, now, required
from services import warehouse


def open_repair(db, car_id, work, rental_id=None):
    get(db.cars, car_id, "Avtomobil")
    work = required(work, "Ish turi")
    cars.take(db, car_id, "repair")
    return db.repairs.insert_one({
        "car_id": car_id, "rental_id": rental_id, "work": work, "parts": [],
        "cost": 0, "status": "open", "created_at": now()}).inserted_id


def _open(db, repair_id):
    doc = get(db.repairs, repair_id, "Buyurtma")
    if doc["status"] != "open":
        raise AppError("Buyurtma yopilgan")
    return doc


def use_part(db, repair_id, part_id, qty):
    doc = _open(db, repair_id)
    car = get(db.cars, doc["car_id"], "Avtomobil")
    part = warehouse.issue(db, part_id, qty, repair_id)
    db.repairs.update_one({"_id": repair_id}, {"$push": {"parts": {
        "part_id": part_id, "name": part["name"], "qty": qty, "price": part["price"],
        "mileage": car["mileage"], "date": date.today().isoformat()}}})


def close(db, repair_id, service_fee):
    doc = _open(db, repair_id)
    if service_fee < 0:
        raise AppError("Xizmat haqi manfiy bo'lmaydi")
    cost = service_fee + sum(p["qty"] * p["price"] for p in doc["parts"])
    db.repairs.update_one({"_id": repair_id}, {"$set": {
        "status": "done", "cost": cost, "closed_at": now()}})
    cars.release(db, doc["car_id"])
    return cost


def maintenance_due(db, today=None, km_margin=500, day_margin=14):
    """Qismi almashtirish muddatiga yaqinlashgan avtomobillar."""
    today = today or date.today()
    latest = {}
    for order in db.repairs.find({}):
        for used in order["parts"]:
            key = (order["car_id"], used["part_id"])
            if key not in latest or (used["date"], used["mileage"]) > (
                    latest[key]["date"], latest[key]["mileage"]):
                latest[key] = used
    due = []
    for (car_id, part_id), used in latest.items():
        car = get(db.cars, car_id, "Avtomobil")
        part = get(db.parts, part_id, "Qism")
        by_km = (part["interval_km"] and
                 car["mileage"] >= used["mileage"] + part["interval_km"] - km_margin)
        by_time = False
        if part["interval_months"]:
            deadline = date.fromisoformat(used["date"]) + timedelta(
                days=30 * part["interval_months"])
            by_time = today >= deadline - timedelta(days=day_margin)
        if by_km or by_time:
            due.append((car, part))
    return due

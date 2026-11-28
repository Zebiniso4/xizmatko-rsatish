"""Ehtiyot qismlar ombori. Qoldiq = jami kirim - jami chiqim."""
from errors import AppError
from models.common import get, now, positive, required


def add_part(db, name, maker, price, min_stock=1, interval_km=0, interval_months=0):
    return db.parts.insert_one({
        "name": required(name, "Nomi"),
        "maker": required(maker, "Ishlab chiqaruvchi"),
        "price": positive(price, "Narx"),
        "min_stock": min_stock,
        "interval_km": interval_km,
        "interval_months": interval_months,
        "stock": 0,
        "movements": [],
    }).inserted_id


def receive(db, part_id, qty):
    positive(qty, "Miqdor")
    part = get(db.parts, part_id, "Qism")
    db.parts.update_one({"_id": part_id}, {
        "$inc": {"stock": qty},
        "$push": {"movements": {"type": "in", "qty": qty, "price": part["price"],
                                "date": now()}}})


def issue(db, part_id, qty, repair_id):
    positive(qty, "Miqdor")
    get(db.parts, part_id, "Qism")
    # Shart va ayirish bitta amalda: qoldiq manfiy bo'lib qolmaydi.
    result = db.parts.update_one({"_id": part_id, "stock": {"$gte": qty}}, {
        "$inc": {"stock": -qty},
        "$push": {"movements": {"type": "out", "qty": qty, "repair_id": repair_id,
                                "date": now()}}})
    if result.modified_count != 1:
        raise AppError("Omborda yetarli qism yo'q")
    return get(db.parts, part_id, "Qism")


def low_stock(db):
    return [p for p in db.parts.find({}) if p["stock"] < p["min_stock"]]

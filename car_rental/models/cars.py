from errors import AppError
from models.common import get, now, positive, required


def add(db, brand, model, year, plate_number, daily_price, mileage=0):
    plate = required(plate_number, "Davlat raqami").upper().replace(" ", "")
    if db.cars.find_one({"plate_number": plate}):
        raise AppError("Bu davlat raqamli avtomobil bor")
    return db.cars.insert_one({
        "brand": required(brand, "Marka"),
        "model": required(model, "Model"),
        "year": positive(year, "Yil"),
        "plate_number": plate,
        "daily_price": positive(daily_price, "Kunlik narx"),
        "mileage": mileage,
        "status": "free",
        "created_at": now(),
    }).inserted_id


def set_price(db, car_id, daily_price):
    get(db.cars, car_id, "Avtomobil")
    db.cars.update_one({"_id": car_id},
                       {"$set": {"daily_price": positive(daily_price, "Kunlik narx")}})


def take(db, car_id, new_status):
    """Faqat bo'sh avtomobilni band qiladi (bitta atomar amal)."""
    result = db.cars.update_one({"_id": car_id, "status": "free"},
                                {"$set": {"status": new_status}})
    if result.modified_count != 1:
        raise AppError("Avtomobil bo'sh emas")


def release(db, car_id):
    db.cars.update_one({"_id": car_id}, {"$set": {"status": "free"}})


def all_cars(db, status=None):
    return list(db.cars.find({"status": status} if status else {}))

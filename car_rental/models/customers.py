from errors import AppError
from models.common import now, required


def add(db, full_name, phone, passport, license_number, address=""):
    passport = required(passport, "Pasport").upper().replace(" ", "")
    if db.customers.find_one({"passport": passport}):
        raise AppError("Bu pasportli mijoz bor")
    return db.customers.insert_one({
        "full_name": required(full_name, "F.I.Sh."),
        "phone": required(phone, "Telefon"),
        "passport": passport,
        "license_number": required(license_number, "Guvohnoma"),
        "address": address.strip(),
        "created_at": now(),
    }).inserted_id


def search(db, text=""):
    text = text.strip().lower()
    return [c for c in db.customers.find({})
            if text in f"{c['full_name']} {c['phone']} {c['passport']}".lower()]


def history(db, customer_id):
    return list(db.rentals.find({"customer_id": customer_id}))

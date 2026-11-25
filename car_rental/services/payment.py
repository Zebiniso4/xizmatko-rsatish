"""To'lovlar va qarzdorlik."""
from errors import AppError
from models.common import get, now, positive

METHODS = ("naqd", "karta")


def paid(db, key, _id):
    return sum(p["amount"] for p in db.payments.find({key: _id}))


def pay(db, amount, method, rental_id=None, repair_id=None):
    positive(amount, "Summa")
    if method not in METHODS:
        raise AppError("To'lov turi: naqd yoki karta")
    if (rental_id is None) == (repair_id is None):
        raise AppError("Ijara yoki ta'mir ko'rsatilishi kerak")
    if rental_id is not None:
        key, _id = "rental_id", rental_id
        due = get(db.rentals, _id, "Ijara")["total"]
    else:
        key, _id = "repair_id", repair_id
        doc = get(db.repairs, _id, "Buyurtma")
        if doc["status"] != "done":
            raise AppError("Avval buyurtmani yoping")
        due = doc["cost"]
    if amount > due - paid(db, key, _id):
        raise AppError("To'lov qarzdan katta")
    return db.payments.insert_one({
        key: _id, "amount": amount, "method": method, "date": now()}).inserted_id


def debts(db):
    """{customer_id: qarz}. Ijaradagi shikast ta'miri ham mijoz hisobiga yoziladi."""
    result = {}
    for rental in db.rentals.find({}):
        debt = rental["total"] - paid(db, "rental_id", rental["_id"])
        for order in db.repairs.find({"rental_id": rental["_id"], "status": "done"}):
            debt += order["cost"] - paid(db, "repair_id", order["_id"])
        if debt > 0:
            cid = rental["customer_id"]
            result[cid] = result.get(cid, 0) + debt
    return result

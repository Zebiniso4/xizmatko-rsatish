"""Hisobotlar."""
from collections import Counter

from models.common import get
from services import payment


def monthly(db, year, month):
    """(tushum, xarajat). Xarajat - shu oyda omborga olingan qismlar."""
    def inside(moment):
        return (moment.year, moment.month) == (year, month)

    income = sum(p["amount"] for p in db.payments.find({}) if inside(p["date"]))
    expense = sum(m["qty"] * m["price"] for part in db.parts.find({})
                  for m in part["movements"] if m["type"] == "in" and inside(m["date"]))
    return income, expense


def top_cars(db, limit=5):
    counts = Counter(r["car_id"] for r in db.rentals.find({}))
    return [(get(db.cars, car_id, "Avtomobil"), n) for car_id, n in counts.most_common(limit)]


def debtors(db):
    return [(get(db.customers, cid, "Mijoz"), debt)
            for cid, debt in payment.debts(db).items()]

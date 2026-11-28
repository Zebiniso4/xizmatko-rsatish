from datetime import date

import pytest

import reports
from errors import AppError
from models import cars, customers
from services import payment, rental, repair, warehouse
from tests.fake_db import FakeDB

D1, D5, D7 = date(2026, 11, 18), date(2026, 11, 22), date(2026, 11, 24)


@pytest.fixture
def setup():
    db = FakeDB()
    car = cars.add(db, "Chevrolet", "Malibu", 2022, "01 a 123 bc", 350000, 1000)
    who = customers.add(db, "Ali Valiyev", "+998901234567", "AA1234567", "AF111")
    return db, car, who


def status(db, car):
    return db.cars.find_one({"_id": car})["status"]


def test_rental_total_and_no_double_booking(setup):
    db, car, who = setup
    rid = rental.open_rental(db, car, who, D1, D5)
    assert db.rentals.find_one({"_id": rid})["total"] == 1_400_000
    assert status(db, car) == "rented"
    with pytest.raises(AppError):
        rental.open_rental(db, car, who, D1, D5)


def test_late_return_with_damage_and_debt(setup):
    db, car, who = setup
    rid = rental.open_rental(db, car, who, D1, D5)
    order = rental.close(db, rid, D7, 1500, "bamper")
    assert db.rentals.find_one({"_id": rid})["total"] == 2_100_000
    assert status(db, car) == "repair"
    assert repair.close(db, order, 200_000) == 200_000
    assert status(db, car) == "free"
    payment.pay(db, 2_100_000, "naqd", rental_id=rid)
    assert payment.debts(db) == {who: 200_000}
    payment.pay(db, 200_000, "karta", repair_id=order)
    assert reports.debtors(db) == []
    with pytest.raises(AppError):
        payment.pay(db, 1, "naqd", rental_id=rid)


def test_stock_and_maintenance(setup):
    db, car, _ = setup
    part = warehouse.add_part(db, "Yog' filtri", "Bosch", 50_000, 2, 5000, 6)
    warehouse.receive(db, part, 3)
    order = repair.open_repair(db, car, "moy almashtirish")
    with pytest.raises(AppError):
        repair.use_part(db, order, part, 4)
    repair.use_part(db, order, part, 2)
    assert repair.close(db, order, 30_000) == 130_000
    assert [p["stock"] for p in warehouse.low_stock(db)] == [1]
    assert repair.maintenance_due(db, today=date.today()) == []
    db.cars.update_one({"_id": car}, {"$set": {"mileage": 5600}})
    assert len(repair.maintenance_due(db)) == 1


def test_duplicates_and_extend(setup):
    db, car, who = setup
    with pytest.raises(AppError):
        cars.add(db, "X", "Y", 2020, "01A123BC", 1)
    rid = rental.open_rental(db, car, who, D1, D5)
    assert rental.extend(db, rid, D7) == 2_100_000
    with pytest.raises(AppError):
        rental.extend(db, rid, D5)

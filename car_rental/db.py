"""MongoDB ulanishi va indekslar."""
import os


def get_db():
    from pymongo import MongoClient

    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    client.admin.command("ping")
    db = client["car_rental"]
    ensure_indexes(db)
    return db


def ensure_indexes(db):
    db.cars.create_index("plate_number", unique=True)
    db.customers.create_index("passport", unique=True)
    db.rentals.create_index("status")

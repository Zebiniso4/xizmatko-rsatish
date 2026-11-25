from datetime import datetime

from errors import AppError


def now():
    return datetime.now()


def required(value, name):
    value = str(value).strip()
    if not value:
        raise AppError(f"{name} bo'sh bo'lmasligi kerak")
    return value


def positive(value, name):
    if value <= 0:
        raise AppError(f"{name} noldan katta bo'lishi kerak")
    return value


def get(collection, _id, name):
    doc = collection.find_one({"_id": _id})
    if doc is None:
        raise AppError(f"{name} topilmadi")
    return doc

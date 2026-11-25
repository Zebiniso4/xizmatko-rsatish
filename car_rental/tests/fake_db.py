"""Testlar uchun xotiradagi soddalashtirilgan MongoDB o'rnini bosuvchi."""
import copy
from itertools import count
from types import SimpleNamespace


class Collection:
    def __init__(self):
        self.docs = []
        self.ids = count(1)

    def _match(self, doc, query):
        for key, want in query.items():
            if isinstance(want, dict):
                if not doc.get(key, 0) >= want["$gte"]:
                    return False
            elif doc.get(key) != want:
                return False
        return True

    def insert_one(self, doc):
        doc = {**copy.deepcopy(doc), "_id": next(self.ids)}
        self.docs.append(doc)
        return SimpleNamespace(inserted_id=doc["_id"])

    def find(self, query):
        return [copy.deepcopy(d) for d in self.docs if self._match(d, query)]

    def find_one(self, query):
        return next(iter(self.find(query)), None)

    def update_one(self, query, update):
        for doc in self.docs:
            if self._match(doc, query):
                doc.update(update.get("$set", {}))
                for key, value in update.get("$inc", {}).items():
                    doc[key] += value
                for key, value in update.get("$push", {}).items():
                    doc[key].append(value)
                return SimpleNamespace(modified_count=1)
        return SimpleNamespace(modified_count=0)


class FakeDB:
    def __init__(self):
        for name in ("cars", "customers", "rentals", "repairs", "parts", "payments"):
            setattr(self, name, Collection())

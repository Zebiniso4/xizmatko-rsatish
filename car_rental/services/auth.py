"""Administrator paroli. Parol kodda saqlanmaydi, ADMIN_PASSWORD orqali beriladi."""
import hmac
import os


def required_password():
    return os.getenv("ADMIN_PASSWORD", "")


def check(entered, expected):
    return bool(expected) and hmac.compare_digest(entered.encode(), expected.encode())

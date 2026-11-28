"""Kiritilgan qiymatlarni tekshirish."""

MAX_MILEAGE = 2_000_000


def valid_mileage(x):
    return isinstance(x, int) and not isinstance(x, bool) and 0 <= x <= MAX_MILEAGE

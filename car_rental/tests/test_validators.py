import pytest

from models.validators import MAX_MILEAGE, valid_mileage


@pytest.mark.parametrize("value, expected", [
    (0, True),
    (MAX_MILEAGE, True),
    (-1, False),
    (MAX_MILEAGE + 1, False),
    (True, False),
    ("90", False),
])
def test_valid_mileage(value, expected):
    assert valid_mileage(value) is expected

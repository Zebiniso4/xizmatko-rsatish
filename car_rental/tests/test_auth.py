from services import auth


def test_password_check():
    assert auth.check("sir123", "sir123")
    assert not auth.check("xato", "sir123")
    assert not auth.check("", "")

import pytest

from app import db
from app.users.models import User


@pytest.fixture(scope="module")
def setup():
    session = db.get_session()
    yield session

    q = User.objects.filter(email="test@test.com")
    if q.count() != 0:
        q.delete()

    session.shutdown()


def test_create_user(setup):
    User.create_user(email="test@test.com", password="123456")


def test_duplicate_users(setup):
    with pytest.raises(Exception):
        User.create_user(email="test@test.com", password="123456")


def test_invalid_email(setup):
    with pytest.raises(Exception):
        User.create_user(email="test@test", password="123456")


def test_valid_password(setup):
    q = User.objects.filter(email="test@test.com")
    assert q.count() == 1

    user_obj = q.first()
    assert user_obj.verify_password("123456") == True
    assert user_obj.verify_password("123456789") == False

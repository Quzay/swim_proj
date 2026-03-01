from .factories import UserFactory
from app.model import User , db , UserRole
import pytest
from sqlalchemy.exc import IntegrityError

def test_create_user(db_session):
    user = UserFactory(username = "Maks")
    db_session.commit()

    assert user.id is not None

def test_user_default_role(db_session):
    user = User(username="NewUser", email="new@test.com", password_hash="123")
    db_session.add(user)
    db_session.commit()
    assert user.role == UserRole.USER


def test_user_age_limits(db_session):
    with pytest.raises(IntegrityError):
        invalid_user = UserFactory(age=-5)
        db_session.commit()
    db_session.rollback()
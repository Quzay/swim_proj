from .factories import UserFactory
from app.model import User , db , UserRole
import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def test_create_user(db_session):
    user = UserFactory()
    db_session.flush()

    assert user.id is not None

def test_user_default_role(db_session):
    user = UserFactory()
    db_session.add(user)
    db_session.flush()
    assert user.role == UserRole.USER


def test_user_age_limits(db_session):
    with pytest.raises(IntegrityError):
        invalid_user = UserFactory(age=-5)
        db_session.flush()
    db_session.rollback()


def test_user_password_hashing(db_session):
    password = "secret_password_123"
    user = UserFactory(password_hash=password)
    db_session.flush()
    assert user.password_hash != password 
    assert len(user.password_hash) > 10

def test_user_timestamps(db_session):
    user = UserFactory()
    db_session.flush()

    assert user.created_at is not None
    assert isinstance(user.created_at, datetime)
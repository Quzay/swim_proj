import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import factory
from app.model import db , User , UserRole
from app import create_app
from .factories import factories
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='session')
def app():
    config = {
        "TESTING" : True,
        "SQLALCHEMY_DATABASE_URI":"postgresql+psycopg://makson:nobodyknow@localhost:5432/pytest",
        "JWT_SECRET_KEY": "test-secret-key-at-least-32-characters-long-12345"
    }
    _app = create_app(config=config)
    return _app

@pytest.fixture(scope='session')
def engine(app):
    with app.app_context():
        return db.engine

@pytest.fixture(scope='session')
def setup_db(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.engine.dispose()
        db.drop_all()


@pytest.fixture(scope="function")
def db_session(app, engine, setup_db):
    with app.app_context():
        connection = engine.connect()
        transaction = connection.begin()

        session = db.session
        session.bind = connection
        for factory_class in factories:
            factory_class._meta.sqlalchemy_session = session
            factory_class.reset_sequence(0)

        yield session

        session.remove()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def auth_header(client):
    client.post("/user/register", json={
        "username": "test",
        "email": "test@gmail.com",
        "password": "testpass",
        "age": 25
    })
    response = client.post("/user/login", json={
        "email": "test@gmail.com",
        "password": "testpass"
    })
    data = response.get_json()
    access_token = data["tokens"]["access"]
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture(scope="function")
def admin_auth_header(client):
    client.post("/user/register", json={
        "username": "testadmin",
        "email": "testadmin@gmail.com",
        "password": "testadminpass",
        "age": 25,
        "role" :"ADMIN"
    })
    response = client.post("/user/login", json={
        "email": "testadmin@gmail.com",
        "password": "testadminpass"
    })
    data = response.get_json()
    access_token = data["tokens"]["access"]
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
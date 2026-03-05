import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import factory
from app.model import db
from app import create_app
from .factories import factories

@pytest.fixture(scope='session')
def app():
    config = {
        "TESTING" : True,
        "SQLALCHEMY_DATABASE_URI":"postgresql+psycopg://makson:nobodyknow@localhost:5432/pytest"
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

        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
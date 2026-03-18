from sqlalchemy.orm import DeclarativeBase
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
jwt = JWTManager()
oauth = OAuth()
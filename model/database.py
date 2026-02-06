import os
from flask import Flask
from .base import db
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)

url = (os.environ.get("LINK_DB"))
app.config["SQLALCHEMY_DATABASE_URI"] = url

def init_db():
    db.init_app(app)
    with app.app_context():
        db.create_all()

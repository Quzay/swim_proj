import os
from .base import Base
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

Link_db = f"postgresql+psycopg://{user}:{password}@{host}:5432/{db_name}"

engine = create_engine(Link_db, echo=True)


def init_db():
    Base.metadata.create_all(engine)
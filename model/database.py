import os
from .base import Base
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.environ.get("LINK_DB"), echo=True)

def init_db():
    Base.metadata.create_all(engine)
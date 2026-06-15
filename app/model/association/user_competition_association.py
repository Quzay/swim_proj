from sqlalchemy import Table, Column, ForeignKey
from ..base import db

user_competition_association_table = Table(
    "user_competition",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("competition_id", ForeignKey("competition.id"), primary_key=True),
)
import datetime
from .base import db
from sqlalchemy.orm import mapped_column,Mapped, relationship , validates
from sqlalchemy import String,DateTime, func, Enum
from typing import Optional,List
from .association import user_competition_association_table
from .enums import Status

class Competition(db.Model):
    __tablename__ = "competition"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    name:Mapped[str] = mapped_column(String(25))
    location:Mapped[str] = mapped_column(String(100))
    date:Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(), default=func.now())
    is_open:Mapped[bool] = mapped_column(default=True)
    amount:Mapped[int] = mapped_column()
    status:Mapped[Optional[Status]]= mapped_column(Enum(Status) , default=Status.ACTIVE , server_default=Status.ACTIVE)

    ratings:Mapped[List["Rating"]] = relationship(back_populates="competition")
    challenges:Mapped[List["Challenge"]] = relationship(back_populates="competitions", cascade="all, delete-orphan")
    users: Mapped[List["User"]] = relationship(
        secondary=user_competition_association_table,
        back_populates="competitions"
    )


    __table_args__ = (
        db.CheckConstraint("name != ''", name = "ck_competition_name"),
        db.CheckConstraint("location != ''", name = "ck_competition_location")
    )

    def __init__(self, **kwargs):
            self.errors = []
            super(Competition,self).__init__(**kwargs)

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            self.errors.append({"message":"Name cannot be empty"})
        if len(name) > 25:
            self.errors.append({"message":"Max 25 characters"})
        return name

    @validates('location')
    def validate_location(self, key, location):
        if not location or not location.strip():
            self.errors.append({"message":"Location cannot be empty"})
        return location

    # @validates('date')
    # def validate_date(self, key, date):
    #     if date and date < datetime.date(2000, 1, 1):
    #         self.errors.append({"message":"Date cannot be earlier than 2000"})
    #     return date
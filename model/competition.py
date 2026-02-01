from datetime import date
from .base import Base
from sqlalchemy.orm import mapped_column,Mapped, relationship
from sqlalchemy import String,Date
from typing import Optional,List

class Competition(Base):
    __tablename__ = "competition"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    name:Mapped[str] = mapped_column(String(25))
    location:Mapped[str] = mapped_column(String(100))
    date:Mapped[Optional[date]] = mapped_column[Date()]

    achievements:Mapped[List["Achievement"]] = relationship(back_populates="competition")

import datetime
from .base import Base
from sqlalchemy.orm import mapped_column,Mapped, relationship
from sqlalchemy import String,DateTime
from typing import Optional,List
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(40))
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    age: Mapped[Optional[int]]
    password: Mapped[str] = mapped_column(String(30))   #?

    goals:Mapped[List["Goal"]] = relationship(back_populates="user")
    achievements:Mapped[List["Achievement"]] = relationship(back_populates="user")
    ratings:Mapped[List["Rating"]] = relationship(back_populates="user")
    activity:Mapped[List["Activity"]] = relationship(back_populates="user")


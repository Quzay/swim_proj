import datetime
from .base import Base
from sqlalchemy.orm import mapped_column,Mapped, relationship
from sqlalchemy import String,ForeignKey,Time,Float
from typing import Optional,List

class Achievement(Base):
    __tablename__ = "achievement"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    stroke:Mapped[str] = mapped_column(String(15))
    time:Mapped[datetime.time] = mapped_column(Time(precision=3))
    distance: Mapped[float] = mapped_column(Float)

    ratings:Mapped[List["Rating"]] = relationship(back_populates="user")
    equipments:Mapped[Optional[List["Equipment"]]] = relationship(back_populates="achievement")

    competition_id:Mapped[int] = mapped_column(ForeignKey("competition.id"))
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
    

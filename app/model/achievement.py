import datetime
from .enums import Stroke_type
from .base import db
from sqlalchemy.orm import mapped_column,Mapped, relationship
from sqlalchemy import String,ForeignKey,Time,Enum
from typing import Optional,List

class Achievement(db.Model):
    __tablename__ = "achievement"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    stroke:Mapped[Stroke_type] = mapped_column(Enum(Stroke_type))
    time:Mapped[datetime.time] = mapped_column(Time(3))
    distance_meters: Mapped[int] 

    ratings:Mapped[List["Rating"]] = relationship(back_populates="achievement")
    equipments:Mapped[Optional[List["Equipment"]]] = relationship(back_populates="achievement")

    competition_id:Mapped[int] = mapped_column(ForeignKey("competition.id"))
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    user:Mapped["User"] = relationship(back_populates="achievements")
    competition:Mapped["Competition"] = relationship(back_populates="achievements")

import datetime
from .base import db 
from sqlalchemy.orm import mapped_column,Mapped, relationship , validates , column_property
from sqlalchemy import Date , Enum , ForeignKey , select, func
from typing import Optional,List
from .enums import Challenge_status
from .activity import Activity 
from .challenge import Challenge

class User_challenge(db.Model):
    __tablename__ = "user_challenge"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status:Mapped[Challenge_status] = mapped_column(Enum(Challenge_status))
    compleated_at: Mapped[Optional[datetime.date]] = mapped_column(Date())
    
    challenge_id:Mapped[int] = mapped_column(ForeignKey("challenge.id"))
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))

    challenge: Mapped[List["Challenge"]] = relationship(back_populates="user_challenges")
    user: Mapped[List["User"]] = relationship(back_populates="user_challenges")

    current_value:Mapped[int] = column_property(
        select(func.coalesce(func.sum(Activity.distance_meters), 0))
       .join(Challenge, Challenge.id == challenge_id)
       .where(Activity.user_id == user_id , func.date(Activity.day) >= Challenge.created_at)
       .scalar_subquery()
        )
           
    
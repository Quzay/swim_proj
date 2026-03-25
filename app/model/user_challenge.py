import datetime
from .base import db 
from sqlalchemy.orm import mapped_column,Mapped, relationship , validates
from sqlalchemy import String,Date , Enum , ForeignKey
from typing import Optional,List
from .enums import Challenge_status

class User_challenge(db.Model):
    __tablename__ = "user_challenge"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status:Mapped[Challenge_status] = mapped_column(Enum(Challenge_status))
    compleated_at: Mapped[Optional[datetime.date]] = mapped_column(Date())
    
    challenge_id:Mapped[int] = mapped_column(ForeignKey("challenge.id"))
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))

    challenge: Mapped[List["Challenge"]] = relationship(back_populates="user_challenges")
    user: Mapped[List["User"]] = relationship(back_populates="user_challenges")
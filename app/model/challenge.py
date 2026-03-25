import datetime
from .base import db
from sqlalchemy.orm import mapped_column,Mapped, relationship , validates 
from sqlalchemy import String,Date ,Text , ForeignKey
from typing import Optional,List

class Challenge(db.Model):
    __tablename__ = "challenge"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20))
    description:Mapped[Optional[str]] = mapped_column(String(110))
    image: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.date] = mapped_column(Date())
    expired_at: Mapped[datetime.date] = mapped_column(Date())

    user_challenges: Mapped[List["User_challenge"]] = relationship(back_populates="challenge")

    __table_args__ = (
        db.CheckConstraint('expired_at >= CURRENT_DATE' , name = "ck_challange"),
    )

    def get_challenge_by_id(challenge_id):
        return Challange.query.get(challenge_id)
    
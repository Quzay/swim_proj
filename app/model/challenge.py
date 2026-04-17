import datetime
from .base import db
from sqlalchemy.orm import mapped_column,Mapped, relationship , validates 
from sqlalchemy import String, ForeignKey , Enum
from typing import Optional,List
from .enums import Stroke_type


class Challenge(db.Model):
    __tablename__ = "challenge"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20))
    description:Mapped[Optional[str]] = mapped_column(String(110))
    distance:Mapped[int] = mapped_column()
    stroke:Mapped[Stroke_type] = mapped_column(Enum(Stroke_type))

    competition_id:Mapped[int] = mapped_column(ForeignKey("competition.id"))
    competitions: Mapped["Competition"] = relationship(back_populates="challenges")
    
    # __table_args__ = (
    #     db.CheckConstraint('expired_at >= CURRENT_DATE' , name = "ck_challange"),
    # )

    @classmethod
    def get_by_id(cls,challenge_id):
        return db.session.get(cls,challenge_id)
    
    def not_in_competition(self, competition_id):
        if self.competition_id != competition_id:
            return True
        return False
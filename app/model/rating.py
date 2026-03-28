from datetime import datetime
from .base import db
from sqlalchemy.orm import mapped_column,Mapped, relationship
from sqlalchemy import ForeignKey, DateTime, func


class Rating(db.Model):
    __tablename__ = "rating"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    created_at:Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())
    value:Mapped[int] 

    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
    achievement_id:Mapped[int] = mapped_column(ForeignKey("achievement.id"))

    user:Mapped["User"] = relationship(back_populates="ratings")
    achievement:Mapped["Achievement"] = relationship(back_populates="ratings")
from datetime import datetime
from .base import Base
from sqlalchemy.orm import mapped_column,Mapped, relationship
from sqlalchemy import ForeignKey, DateTime


class Rating(Base):
    __tablename__ = "rating"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    created_at:Mapped[datetime] = mapped_column(DateTime())
    value:Mapped[int] 

    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
    achievement_id:Mapped[int] = mapped_column(ForeignKey("achievement.id"))

    user:Mapped["User"] = relationship(back_populates="ratings")
    achievement:Mapped["Achievement"] = relationship(back_populates="ratings")
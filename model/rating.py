from datetime import datetime
from .base import Base
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import String,ForeignKey, DateTime
from typing import Optional

class Rating(Base):
    __tablename__ = "rating"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    created_at:Mapped[datetime] = mapped_column(DateTime())
    value:Mapped[int] 

    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
    achievement_id:Mapped[int] = mapped_column(ForeignKey("achievement.id"))
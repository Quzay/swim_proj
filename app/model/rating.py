from datetime import datetime
from .base import db
from sqlalchemy.orm import mapped_column,Mapped, relationship
from sqlalchemy import ForeignKey, DateTime, func, Float



class Rating(db.Model):
    __tablename__ = "rating"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    created_at:Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    value:Mapped[float] = mapped_column(Float(2)) 
    updated_at:Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
    activity_id:Mapped[int] = mapped_column(ForeignKey("activity.id"))
    
    
    user:Mapped["User"] = relationship(back_populates="ratings")
    activity:Mapped["Activity"] = relationship(back_populates="ratings")
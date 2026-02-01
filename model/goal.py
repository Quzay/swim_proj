import datetime
from .base import Base
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import String,ForeignKey,DateTime,Float
from typing import Optional,List

class Goal(Base):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    distance: Mapped[float] = mapped_column(Float)
    deadline: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))

    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))

    #remaining:

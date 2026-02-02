import datetime
from .base import Base
from .user import User
from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy import ForeignKey,DateTime,Float


class Goal(Base):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    distance: Mapped[float] = mapped_column(Float)
    deadline: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))

    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))

    user:Mapped["User"] = relationship(back_populates="goals")
    #remaining:

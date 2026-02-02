from datetime import datetime
from .base import Base
from sqlalchemy.orm import mapped_column,Mapped, relationship
from sqlalchemy import String,ForeignKey,DateTime,Float

class Activity(Base):
    __tablename__ = "activity"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    day:Mapped[datetime] = mapped_column(DateTime())
    stroke:Mapped[str] = mapped_column(String(15))
    distance: Mapped[float] = mapped_column(Float)

    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))

    user:Mapped["User"] = relationship(back_populates="activity")
from .base import Base
from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy import String,ForeignKey
from typing import Optional


class Equipment(Base):
    __tablename__ = "equipment"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    name:Mapped[Optional[str]] = mapped_column(String(20))
    typ:Mapped[Optional[str]] = mapped_column(String(15))
    brand:Mapped[Optional[str]] = mapped_column(String(25))

    achievement_id:Mapped[int] = mapped_column(ForeignKey("achievement.id"))

    achievement:Mapped["Achievement"] = relationship(back_populates="equipments")
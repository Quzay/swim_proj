from .base import db
from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy import String,ForeignKey, Enum
from typing import Optional
from .enums import Equipment_type

class Equipment(db.Model):
    __tablename__ = "equipment"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    name:Mapped[str] = mapped_column(String(40))
    type:Mapped[Equipment_type] = mapped_column(Enum(Equipment_type))
    brand:Mapped[Optional[str]] = mapped_column(String(50))
    is_broken:Mapped[bool] = mapped_column(default=False)

    activity_id:Mapped[int] = mapped_column(ForeignKey("activity.id"))

    activity:Mapped["Activity"] = relationship(back_populates="equipments")
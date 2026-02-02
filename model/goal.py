import datetime
from .base import Base
from sqlalchemy.orm import mapped_column,Mapped,relationship,column_property
from sqlalchemy import ForeignKey,DateTime,Column

class Goal(Base):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    target_distance: Mapped[int] 
    deadline: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))
    #remaining = column_property(
    #    target_distance = Column 
    #)


    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))

    user:Mapped["User"] = relationship(back_populates="goals")
    

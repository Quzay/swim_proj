import datetime
from .base import Base
from .activity import Activity
from sqlalchemy.orm import mapped_column,Mapped,relationship,column_property
from sqlalchemy import ForeignKey,Date,select,func

class Goal(Base):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    target_distance: Mapped[int] = mapped_column()
    deadline: Mapped[datetime.date] = mapped_column(Date())
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))

    user:Mapped["User"] = relationship(back_populates="goals")

    remaining_distance:Mapped[int] = column_property(
       target_distance - (
        select(func.coalesce(func.sum(Activity.distance_meters), 0))
       .where(Activity.user_id == user_id)
       .correlate_except(Activity)
       .scalar_subquery()
       )    
    )

    days_left = column_property(
        deadline - func.current_date()
    )


    
    

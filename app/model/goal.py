import datetime
from .base import db
from .activity import Activity
from sqlalchemy.orm import mapped_column,Mapped,relationship,column_property, validates
from sqlalchemy import ForeignKey,Date,select,func

class Goal(db.Model):
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

    __table_args__ = (
        db.CheckConstraint('target_distance > 0' , name = "ck_goal_targer_distance"),
    )
    
    @validates('target_distance')
    def validate_target_distance(self, key, target_distance):
        if not target_distance or target_distance <= 0 :
            raise ValueError('Distance can not be negative')
        return target_distance
    
    @validates('deadline') 
    def validete_deadline(self, key , deadline):
        today = datetime.datetime.today().date()
        if deadline and deadline < today:
            raise ValueError("The goal date cannot be in the past")
        return deadline
    
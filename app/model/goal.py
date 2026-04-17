import datetime
from .base import db
from .activity import Activity
from sqlalchemy.orm import mapped_column,Mapped,relationship,column_property, validates
from sqlalchemy import ForeignKey,Date,select,func , DateTime , Enum , extract
from .enums import Status

class Goal(db.Model):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    target_distance: Mapped[int] = mapped_column()
    deadline: Mapped[datetime.datetime] = mapped_column(DateTime(), default=func.now())
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(), default=func.now())
    user:Mapped["User"] = relationship(back_populates="goals")
    status:Mapped[Status] = mapped_column(Enum(Status))

    remaining_distance:Mapped[int] = column_property(
       target_distance - (
        select(func.coalesce(func.sum(Activity.distance_meters), 0))
       .where(Activity.user_id == user_id , Activity.created_at >= created_at , Activity.created_at <= deadline)
       .scalar_subquery()
       )    
    )

    days_left = column_property(
        extract("day" ,deadline - func.now())
    )

    __table_args__ = (
        db.CheckConstraint('target_distance > 0' , name = "ck_goal_target_distance"),
        db.CheckConstraint('deadline >= CURRENT_DATE' , name = "ck_goal_deadline")
    )
    def __init__(self, **kwargs):
            self.errors = []
            super(Goal,self).__init__(**kwargs)
    
    @validates('target_distance')
    def validate_target_distance(self, key, target_distance):
        if type(target_distance) != int:
            self.errors.append('Distance must be number')
        elif target_distance <= 0 :
            self.errors.append('Distance can not be negative')
        return target_distance
    
    @validates('deadline')
    def validate_deadline(self, key, deadline):
        if deadline is None:
            self.errors.append("Deadline is required")
            return None
        deadline_obj = None
        if isinstance(deadline, str):
            try:
                deadline_obj = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                self.errors.append("Deadline format must be YYYY-MM-DD")
        elif isinstance(deadline, (datetime.datetime, datetime.date)):

            deadline_obj = deadline.date() if isinstance(deadline, datetime.datetime) else deadline
        else:
            self.errors.append("Deadline must be a string or a date")
        if deadline_obj:
            if deadline_obj < datetime.date.today():
                self.errors.append("Deadline cannot be in the past")
            return deadline_obj
        return deadline
    
import datetime
from .enums import Stroke_type
from sqlalchemy.orm import mapped_column,Mapped, relationship,validates
from sqlalchemy import String,ForeignKey,DateTime, desc , select, Enum
from .base import db



class Activity(db.Model):
    __tablename__ = "activity"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    day:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.datetime.now(datetime.timezone.utc))
    stroke:Mapped[Stroke_type] = mapped_column(Enum(Stroke_type))
    distance_meters: Mapped[int] 

    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))

    user:Mapped["User"] = relationship(back_populates="activity")

    __table_args__ = (
        db.CheckConstraint('distance_meters > 0 ', name = "ck_activity_distance"),
    )
    def __init__(self, **kwargs):
            self.errors = []
            super(Activity,self).__init__(**kwargs)

    @validates('distance_meters')
    def validate_distance(self, key, distance_meters):
        if type(distance_meters) == int:
            if not distance_meters or distance_meters <=0:
                self.errors.append({'message':'Distance can not be negative'})
        else:
            self.errors.append({"message":"Distance must be int"})
        return distance_meters

    @validates('day')
    def validate_date(self, key, day):
        pass
    
    @validates('stroke')
    def validate_stroke(self, key, stroke):
        if stroke is None or stroke == "":
            self.errors.append({"message":"Stroke is required"})
        return stroke

    @classmethod
    def get_last_by_user_id (cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(desc(cls.id)).first()
    
    @classmethod
    def get_all_activity_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
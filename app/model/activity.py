import datetime
from .enums import Stroke_type, ModelName
from sqlalchemy.orm import mapped_column,Mapped, relationship,validates , column_property
from sqlalchemy import Float,ForeignKey,DateTime, desc , select, Enum  , func , case , exists , cast, Numeric
from .base import db
from typing import List
from .challenge import Challenge



class Activity(db.Model):
    __tablename__ = "activity"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(), default=func.now())
    stroke:Mapped[Stroke_type] = mapped_column(Enum(Stroke_type))
    distance_meters: Mapped[int] = mapped_column()
    time_s:Mapped[float] = mapped_column(Float(3)) 
    model_name:Mapped[ModelName] = mapped_column(Enum(ModelName)) 
    referense_id:Mapped[int]
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))

    speed:Mapped[float] = column_property(
        func.round(
            cast(
                case((time_s>0, distance_meters / time_s),else_=0.0 ), Numeric
            ),2
        )
    )

    user:Mapped["User"] = relationship(back_populates="activity")
    ratings:Mapped[List["Rating"]] = relationship(back_populates="activity")
    equipments:Mapped[List["Equipment"]] = relationship(back_populates="activity")

    __table_args__ = (
        db.CheckConstraint('distance_meters > 0 ', name = "ck_activity_distance"),
        db.CheckConstraint('time_s > 0.1', name = "ck_activity_time")
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

    @validates('time_s')
    def validate_time(self, key, time_s):
        if not isinstance(time_s, (int, float)):
            self.errors.append({"message": "Time must be a number"})
        elif time_s <= 0:
            self.errors.append({"message": "Time must be greater than zero"})
        return time_s
        
    @validates('stroke')
    def validate_stroke(self, key, stroke):
        if stroke not in Stroke_type:
            self.errors.append({"message": "Invalid stroke type"})
        return stroke
    
    @validates('model_name')
    def validate_model_name(self, key, model_name):
        if model_name not in ModelName:
            self.errors.append({"message": "Invalid model name"})
        return model_name
    
    @classmethod
    def get_last_by_user_id (cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(desc(cls.id)).first()
    
    @classmethod
    def get_all_activity_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def already_post(cls,challenge_id:int , user_id:int) -> bool:
        stmt = select(
        exists().where(
            cls.model_name == ModelName.CHALLENGE,
            cls.referense_id == challenge_id,
            cls.user_id == user_id
            )
        )
        return bool(db.session.scalar(stmt))

    def check_require(self,challenge_id) :
        from .rating import Rating
        challenge = db.session.get(Challenge,challenge_id)
        if self.distance_meters>= challenge.distance:
            if self.stroke == challenge.stroke:
                new_rating = Rating(
                    value = 5,
                    user_id = self.user_id,
                    activity_id = self.id,
                )
            db.session.add(new_rating)
            db.session.commit()
            return True
        return False
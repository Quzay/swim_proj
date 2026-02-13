import datetime
import enum
from sqlalchemy.orm import mapped_column,Mapped, relationship,validates
from sqlalchemy import String,ForeignKey,DateTime, desc , select, Enum
from .base import db

class Stroke_type(enum.Enum):
    FREESTYLE = "Freestyle"
    BACKSTROKE = "Backstroke"
    BREASTSTROKE = "Breaststroke"
    BUTTERFLY = "Butterfly"

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
    @validates('distance_meters')
    def validate_distance(self, key, distance_meters):
        if not distance_meters or distance_meters <=0:
            raise ValueError('Distance can not be negative')
        return distance_meters


    @classmethod
    def get_last_by_user_id (cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(desc(cls.id)).first()
    
    @classmethod
    def get_all_activity_by_user(cls, user_id):
        stmt = select(cls).where(cls.user_id == user_id)
        res = db.session.execute(stmt)
        all_activity = res.scalars().all()
        return all_activity
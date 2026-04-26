import datetime
from .base import db
from sqlalchemy.orm import mapped_column,Mapped, relationship , validates 
from sqlalchemy import String, ForeignKey , Enum
from typing import Optional,List
from .enums import Stroke_type


class Challenge(db.Model):
    __tablename__ = "challenge"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20))
    description:Mapped[Optional[str]] = mapped_column(String(110))
    distance:Mapped[int] = mapped_column()
    stroke:Mapped[Stroke_type] = mapped_column(Enum(Stroke_type))

    competition_id:Mapped[int] = mapped_column(ForeignKey("competition.id"))
    competitions: Mapped["Competition"] = relationship(back_populates="challenges")
    
    __table_args__ = (
        db.CheckConstraint("distance > 0", name="ck_challenge_distance"),
        db.CheckConstraint("name != ''", name = "ck_challenge_name")
    )

    def __init__(self, **kwargs):
        self.errors = []
        super(Challenge, self).__init__(**kwargs)
        
    @validates('name')
    def validate_name(self, key, name):
        if not isinstance(name, str):
            self.errors.append({"message": "Challenge name must be a string"})
        elif not name or name.strip() == '':
            self.errors.append({"message": "Challenge name cannot be empty"})
        elif len(name) > 20:
            self.errors.append({"message": "Challenge name is too long (max 20)"})
        return name.strip() if isinstance(name, str) else name

    @validates('distance')
    def validate_distance(self, key, distance):
        if not isinstance(distance, int):
            self.errors.append({"message": "Distance must be an integer"})
        elif distance <= 0:
            self.errors.append({"message": "Distance must be greater than zero"})
        return distance
    
    @validates('stroke')
    def validate_stroke(self, key, stroke):
        if stroke not in Stroke_type:
            self.errors.append({"message": "Invalid stroke type"})
        return stroke
    
    @validates('description')
    def validate_description(self, key, description):
        if description is not None:
            if len(description) > 110:
                self.errors.append({"message": "Description is too long (max 110)"})
        return description    

    @classmethod
    def get_by_id(cls,challenge_id):
        return db.session.get(cls,challenge_id)
    
    def not_in_competition(self, competition_id):
        if self.competition_id != competition_id:
            return True
        return False
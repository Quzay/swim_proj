from datetime import datetime
from .base import db
from sqlalchemy.orm import mapped_column,Mapped, relationship
from sqlalchemy import ForeignKey, DateTime, func, Float, select
from .enums import ModelName


class Rating(db.Model):
    __tablename__ = "rating"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    created_at:Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    value:Mapped[float] = mapped_column(Float(2)) 
    updated_at:Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
    activity_id:Mapped[int] = mapped_column(ForeignKey("activity.id"))
    
    
    user:Mapped["User"] = relationship(back_populates="ratings")
    activity:Mapped["Activity"] = relationship(back_populates="ratings")



    @classmethod
    def calculate_winners(cls,competition_id):
        from .activity import Activity
        from .challenge import Challenge
        challenges = db.session.execute(select(Challenge).where(Challenge.competition_id==competition_id)).scalars().all()
        for challenge in challenges:
            bonus = 3
            top_activities = db.session.execute(select(Activity).
                                             where(Activity.referense_id == challenge.id , Activity.model_name == ModelName.CHALLENGE)
                                             .order_by(Activity.time_s.asc())
                                             .limit(3)
                                             ).scalars().all()
            for activity in top_activities:
                rating = db.session.execute(select(Rating).where(Rating.activity_id == activity.id)).scalar_one_or_none()
                if rating:
                    rating.value += bonus
                    bonus -= 1
                if bonus <= 0:
                    break
        db.session.commit()
        return None #?
    
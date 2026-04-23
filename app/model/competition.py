import datetime
from .base import db
from sqlalchemy.orm import mapped_column,Mapped, relationship , validates
from sqlalchemy import String,DateTime, func, Enum, select, exists
from typing import Optional,List
from .association import user_competition_association_table
from .enums import Status, ModelName

class Competition(db.Model):
    __tablename__ = "competition"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    name:Mapped[str] = mapped_column(String(25))
    location:Mapped[str] = mapped_column(String(100))
    date:Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(), default=func.now())
    is_open:Mapped[bool] = mapped_column(default=True)
    amount:Mapped[int] = mapped_column()
    status:Mapped[Optional[Status]]= mapped_column(Enum(Status) , default=Status.ACTIVE , server_default=Status.ACTIVE)

    challenges:Mapped[List["Challenge"]] = relationship(back_populates="competitions", cascade="all, delete-orphan")
    users: Mapped[List["User"]] = relationship(
        secondary=user_competition_association_table,
        back_populates="competitions"
    )


    __table_args__ = (
        db.CheckConstraint("name != ''", name = "ck_competition_name"),
        db.CheckConstraint("location != ''", name = "ck_competition_location"),
        db.CheckConstraint("amount > 0", name="ck_competition_amount"),
    )

    def __init__(self, **kwargs):
            self.errors = []
            super(Competition,self).__init__(**kwargs)

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            self.errors.append({"message":"Name cannot be empty"})
        if len(name) > 25:
            self.errors.append({"message":"Max 25 characters"})
        return name

    @validates('location')
    def validate_location(self, key, location):
        if not location or not location.strip():
            self.errors.append({"message":"Location cannot be empty"})
        return location

    @validates('amount')
    def validate_amount(self, key, amount):
        if not isinstance(amount, int):
            self.errors.append({"message": "Amount must be an integer"})
        elif amount < 0:
            self.errors.append({"message": "Amount cannot be negative"})
        return amount

    @validates('date')
    def validate_date(self, key, date):
        if date:
            yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)
            if date < yesterday:
                self.errors.append({"message": f"Competition date {datetime.date.strftime('%Y-%m-%d')} cannot be in the past"})
        return date

    @validates('status')
    def validate_status(self, key, status):
        if status not in Status:
            self.errors.append({"message": "Invalid status value"})
        return status

    @classmethod
    def check_participate(cls, competition_id : int, user_id :int) -> bool:
        stmt = select(
        exists().where(
            user_competition_association_table.c.competition_id == competition_id,
            user_competition_association_table.c.user_id == user_id
            )
        )
        return bool(db.session.scalar(stmt))
    
    def current_activity(self):
        from .activity import Activity
        from .challenge import Challenge
        current = db.session.execute(select(func.count(Activity.id))
                                    .join(Challenge, (Activity.referense_id == Challenge.id) & (Activity.model_name == ModelName.CHALLENGE))
                                    .where(Challenge.competition_id == self.id)
                                    ).scalar() or 0
        return current
    
    def expected_activity(self):
        from .challenge import Challenge
        expected = self.amount * db.session.execute(select(func.count())
                                                    .select_from(Challenge)
                                                    .where(Challenge.competition_id == self.id)
                                                    ).scalar()
        return expected
    
    def check_number_of_free_activity(self):
        from .rating import Rating
        if self.current_activity() >= self.expected_activity():
            self.status == Status.COMPLETED
            Rating.calculate_winners(self.id)
            db.session.commit()
            return True
        return False


    
        
    
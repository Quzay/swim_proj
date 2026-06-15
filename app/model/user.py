import hashlib
import datetime
from typing import Optional,List
from .base import db
from sqlalchemy.orm import mapped_column,Mapped, relationship, validates, column_property, declared_attr
from sqlalchemy import String,DateTime,Enum, select
from sqlalchemy.sql import func
from .enums import UserRole
from .association import user_competition_association_table

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(40) , unique=True)
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    age: Mapped[Optional[int]]
    password_hash: Mapped[str] = mapped_column(String(64))   
    role:Mapped[UserRole] = mapped_column(Enum(UserRole),default=UserRole.USER)
    facebook_id:Mapped[Optional[str]] = mapped_column(String(100)) 

    @declared_attr
    def total_rating(cls) -> Mapped[float]:
        from .rating import Rating
        return column_property(select(func.sum(Rating.value))
                               .where(Rating.user_id == cls.id)
                               .correlate_except(Rating)
                               .scalar_subquery())
    @declared_attr
    def activity_count(cls) -> Mapped[int]:
        from .activity import Activity
        return column_property(select(func.count(Activity.id))
                               .where(Activity.user_id == cls.id)
                               .correlate_except(Activity)
                               .scalar_subquery())
    @declared_attr
    def total_distance(cls) -> Mapped[int]:
        from .activity import Activity
        return column_property(select(func.sum(Activity.distance_meters))
                               .where(Activity.user_id == cls.id)
                               .correlate_except(Activity)
                               .scalar_subquery())
    
    goals:Mapped[List["Goal"]] = relationship(back_populates="user",cascade="all, delete-orphan")
    ratings:Mapped[List["Rating"]] = relationship(back_populates="user",cascade="all, delete-orphan")
    activity:Mapped[List["Activity"]] = relationship(back_populates="user",cascade="all, delete-orphan")
    
    competitions: Mapped[List["Competition"]] = relationship(
        secondary=user_competition_association_table,
        back_populates="users"
    )
    __table_args__ = (
        db.UniqueConstraint('email', name='uq_user_email'),
        db.CheckConstraint('age BETWEEN 5 and 100', name='ck_user_age'),
        db.CheckConstraint("username != ''", name='ck_user_username_not_empty'),
        db.CheckConstraint("email LIKE '%_@__%.__%'", name='ck_user_email_format'),
    )
    def __init__(self, **kwargs):
        self.errors = []
        super(User,self).__init__(**kwargs)

    @validates('email')
    def validate_email(self, key, email):
        if type(email) != str:
            self.errors.append({"message":"Email must be string"})
        if not email or '@' not in email:
            self.errors.append({"message":"Invalid email format"})
        return email

    @validates('age')
    def validate_age(self, key, age):
        if type(age) != int:
            self.errors.append({"message":"Age must be int"})
        if age is not None and (age < 5 or age > 100):
            self.errors.append({"message":"Age must be between 5 and 100"})
        return age
    
    @validates('username')
    def validate_username(self, key, username):
        if type(username) != str:
            self.errors.append({"message":"Username must be string"})
        if not username or username.strip() == '':
            self.errors.append({"message":"Username cannot be empty"})
        return username.strip()

    @validates('password_hash')
    def validate_password(self, key, password_hash):
        if type(password_hash) != str:
            self.errors.append({"message":"Password must be string"})
        if not password_hash or password_hash.strip() == '':
            self.errors.append({"message":"Password cannot be empty"})
        return password_hash.strip()


    def set_password(self, password:str):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password:str) -> bool:
        entered_password_hash = hashlib.sha256(password.encode()).hexdigest()
        if entered_password_hash == self.password_hash:
            return True
        else:
            return False
    
    @classmethod
    def find_by_email(cls, email):
       return db.session.execute(select(cls).filter_by(email=email)).scalar_one_or_none()
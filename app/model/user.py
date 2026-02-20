import datetime
from typing import Optional,List
from .base import db
from sqlalchemy.orm import mapped_column,Mapped, relationship, validates
from sqlalchemy import String,DateTime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(40) , unique=True)
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    age: Mapped[Optional[int]]
    password_hash: Mapped[str] = mapped_column(String(256))   #?

    goals:Mapped[List["Goal"]] = relationship(back_populates="user",cascade="all, delete-orphan")
    achievements:Mapped[List["Achievement"]] = relationship(back_populates="user",cascade="all, delete-orphan")
    ratings:Mapped[List["Rating"]] = relationship(back_populates="user",cascade="all, delete-orphan")
    activity:Mapped[List["Activity"]] = relationship(back_populates="user",cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint('email', name='uq_user_email'),
        db.CheckConstraint('age BETWEEN 5 and 100', name='ck_user_age'),
        db.CheckConstraint("username != ''", name='ck_user_username_not_empty'),
        db.CheckConstraint("email LIKE '%_@__%.__%'", name='ck_user_email_format'),
    )

    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError("Invalid email format")
        return email
    
    @validates('age')
    def validate_age(self, key, age):
        if type(age) != int:
            raise ValueError("Age must be int")
        if age is not None and (age < 5 or age > 100):
            raise ValueError("Age must be between 5 and 100")
        return age
    
    @validates('username')
    def validate_username(self, key, username):
        if type(username) != str:
            raise ValueError("Username must be string")
        if not username or username.strip() == '':
            raise ValueError("Username cannot be empty")
        return username.strip()
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
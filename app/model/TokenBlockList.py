from .base import db
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import DateTime,func
from datetime import datetime


class TokenBlockList(db.Model):
    __table_name__ = "tokenblocklost"
    id:Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    jti: Mapped[str] = mapped_column()
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Token {self.jti}"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
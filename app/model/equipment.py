from .base import db
from sqlalchemy.orm import mapped_column,Mapped,relationship, validates
from sqlalchemy import String,ForeignKey, Enum
from typing import Optional
from .enums import Equipment_type


class Equipment(db.Model):
    __tablename__ = "equipment"

    id:Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    name:Mapped[str] = mapped_column(String(40))
    type:Mapped[Equipment_type] = mapped_column(Enum(Equipment_type))
    brand:Mapped[Optional[str]] = mapped_column(String(50))
    is_broken:Mapped[bool] = mapped_column(default=False)

    activity_id:Mapped[int] = mapped_column(ForeignKey("activity.id"))

    activity:Mapped["Activity"] = relationship(back_populates="equipments")

    __table_args__ = (
        db.CheckConstraint("name != ''", name = "ck_equipment_name"),
        db.CheckConstraint("brand IS NULL OR brand != ''", name = "ck_equipment_brand"),
    )

    def __init__(self, **kwargs):
            self.errors = []
            super(Equipment,self).__init__(**kwargs)

    @validates('name')
    def validate_name(self, key, name):
        if not isinstance(name, str):
            self.errors.append({"message":"Name must be string"})
        if not name or name.strip() == '':
            self.errors.append({"message":"Name cannot be empty"})
        if len(name) > 40:
            self.errors.append({"message":"Max 40 characters"})
        return name
    
    @validates("brand")
    def validate_brand(self, key, brand):
        if brand is not None:
            if not isinstance(brand, str):
                self.errors.append({"message": "Brand must be a string"})
            elif brand.strip() == '':
                self.errors.append({"message": "Brand cannot be an empty string"})
            return brand.strip()
        return brand
    
    def validate_type(self, key, equipment_type):
        if equipment_type not in Equipment_type:
            self.errors.append({"message": f"Invalid equipment type. Must be one of {[e.value for e in Equipment_type]}"})
        return equipment_type
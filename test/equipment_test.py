from .factories import EquipmentFactory , ActivityFactory, RatingFactory
from app.model import Equipment, db 
import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime 
from sqlalchemy import select

def test_equipment_invalid_name():
    eq1 = EquipmentFactory(name="  ")
    assert any("Name cannot be empty" in err["message"] for err in eq1.errors)
    eq2 = EquipmentFactory(name="a" * 41)
    assert any("Max 40 characters" in err["message"] for err in eq2.errors)

def test_equipment_invalid_brand():
    eq = EquipmentFactory(brand="   ")
    assert any("Brand cannot be an empty string" in err["message"] for err in eq.errors)

def test_equipment_invalid_type():
    eq = EquipmentFactory(type="SUPER_FLIPPERS")
    assert any("Invalid equipment type" in err["message"] for err in eq.errors)

def test_equipment_default_status():
    eq = EquipmentFactory()
    assert eq.is_broken is False

@pytest.mark.integration
def test_create_equipment_success(client, admin_auth_header):
    from app.model import User
    admin = db.session.scalar(select(User).where(User.email == "testadmin@gmail.com"))
    
    act = ActivityFactory(user = admin)
    db.session.commit()
    
    payload = {
        "name": "Flippers Speedo",
        "type": "FLIPPERS", 
        "brand": "Speedo",
        "activity_id": act.id
    }
    response = client.post(f"/activity/{act.id}/equipment", json=payload, headers=admin_auth_header)
    assert response.status_code == 200

@pytest.mark.integration
def test_break_equipment(client, admin_auth_header):
    from app.model import User, Rating
    admin = db.session.scalar(select(User).where(User.email == "testadmin@gmail.com"))
    
    act = ActivityFactory(user = admin)
    db.session.commit()
    rating = RatingFactory(activity_id = act.id, user = admin)
    payload = {
        "name": "Fanks Speedo",
        "type": "FLIPPERS", 
        "brand": "Speedo",
        "activity_id": act.id
    }
    response = client.post(f"/activity/{act.id}/equipment", json=payload, headers=admin_auth_header)
    assert response.status_code == 200

    eq = db.session.scalar(select(Equipment).where(Equipment.activity_id == act.id))
    response_1 = client.put(f'/activity/{act.id}/equipment/{eq.id}' , headers=admin_auth_header)
    assert response_1.status_code == 200
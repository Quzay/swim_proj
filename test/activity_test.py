from .factories import ActivityFactory, UserFactory
from app.model import Activity , db , Stroke_type
import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime


def test_activity_validation_success(db_session):
    user = UserFactory()
    db.session.flush()

    act = ActivityFactory(user=user)
    db.session.flush()
    assert act.id is not None
    

def test_activity_negative_distance(db_session):
    act = ActivityFactory( distance_meters=-10)
    assert any("Distance can not be negative" in e['message'] for e in act.errors)

def test_activity_invalid_stroke_type(db_session):
    act = ActivityFactory(stroke=None)
    assert any("Stroke is required" in e['message'] for e in act.errors)


#Integration
def test_create_activity_api_success(client, auth_header):
    payload = {
        "stroke": "FREESTYLE",
        "distance_meters": 1500
    }
    response = client.post("/activity/", json=payload, headers=auth_header)
    
    assert response.status_code == 200
    assert response.json["message"] == "Activity was succesful created"

def test_create_activity_invalid_enum(client, auth_header):
    payload = {
        "stroke": "DOGGY_PADDLE",
        "distance_meters": 50
    }
    response = client.post("/activity/", json=payload, headers=auth_header)
   
    assert response.status_code != 200 

def test_create_activity_unauthorized(client):
    response = client.post("/activity/", json={"stroke": "BACKSTROKE", "distance_meters": 100})
    assert response.status_code == 401
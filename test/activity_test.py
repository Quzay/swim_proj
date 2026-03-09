from .factories import ActivityFactory
from app.model import Activity , db , Stroke_type
import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime


def test_activity_validation_success():
    act = Activity(stroke=Stroke_type.FREESTYLE, distance_meters=500, user_id=1)
    assert len(act.errors) == 0
    assert act.distance_meters == 500

def test_activity_negative_distance():
    act = Activity(stroke=Stroke_type.BUTTERFLY, distance_meters=-10, user_id=1)
    assert any("Distance can not be negative" in e['message'] for e in act.errors)

def test_activity_invalid_stroke_type():
    act = Activity(stroke=None, distance_meters=100, user_id=1)
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
from .factories import ActivityFactory, UserFactory, CompetitionFactory, ChallengeFactory
from app.model import Activity , db , Stroke_type 
import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime


def test_activity_validation_success(user):
    act = ActivityFactory(user=user)
    db.session.flush()
    assert act.id is not None

def test_activity_negative_distance(db_session):
    act = ActivityFactory(distance_meters=-10)
    with pytest.raises(IntegrityError) as excinfo:
        db_session.flush()
    assert "ck_activity_distance" in str(excinfo.value)

def test_activity_invalid_stroke_type(db_session):
    act = ActivityFactory(stroke=None)
    assert act.id is None

def test_activity_speed_calculate(user):
    act = ActivityFactory(distance_meters = 1000, time_s = 100, user = user)
    db.session.flush()
    assert act.id is not None
    assert act.speed == 10.0


#Integration
@pytest.mark.integration
def test_create_activity_api_success(client, auth_header):
    compet = CompetitionFactory()
    db.session.add(compet)
    db.session.flush()
    challenge = ChallengeFactory(competition_id = compet.id)
    db.session.add(challenge)
    db.session.flush()
    payload = {
        "stroke": "FREESTYLE",
        "distance_meters": 1500,
        "time_s" : 140.2,
    }
    response_1 = client.post(f"/competition/{compet.id}/join/" , headers = auth_header)
    assert response_1.status_code == 200

    response = client.post(f"/competition/{compet.id}/challenge/{challenge.id}/activity", json=payload, headers=auth_header)
    assert response.status_code == 200
       
@pytest.mark.integration
def test_create_activity_invalid_enum(client, auth_header):
    payload = {
        "stroke": "DOGGY_PADDLE",
        "distance_meters": 50
    }
    response = client.post("/activity/", json=payload, headers=auth_header)
   
    assert response.status_code != 200 

@pytest.mark.integration
def test_create_activity_unauthorized(client, auth_header):
    compet = CompetitionFactory()
    db.session.add(compet)
    db.session.flush()
    challenge = ChallengeFactory(competition_id = compet.id)
    db.session.add(challenge)
    db.session.flush()
    
    response_1 = client.post(f"/competition/{compet.id}/join/" ,  headers = auth_header)
    assert response_1.status_code == 200
    
    response = client.post(f"/competition/{compet.id}/challenge/{challenge.id}/activity", json={"stroke": "BACKSTROKE", "distance_meters": 100})
    assert response.status_code == 401
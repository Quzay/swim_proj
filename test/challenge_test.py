from .factories import ChallengeFactory , CompetitionFactory
from app.model import Challenge , db 
import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime 

def test_valid_model(competition):
    chal = ChallengeFactory(competitions = competition)
    db.session.flush()
    assert chal.id is not None

def test_challenge_negative_distance(competition):
    chal = ChallengeFactory(distance = -10, competitions = competition)
    with pytest.raises(IntegrityError) as excinfo:
        db.session.flush()
    assert "ck_challenge_distance" in str(excinfo.value)

def test_challenge_empty_name(db_session):
    chal = ChallengeFactory(name=" ")
    assert any("cannot be empty" in err["message"] for err in chal.errors)

def test_challenge_description_too_long(db_session):
    long_desc = "a" * 111
    chal = ChallengeFactory(description=long_desc)
    assert any("Description is too long" in err["message"] for err in chal.errors)

def test_challenge_invalid_stroke(db_session):
    chal = ChallengeFactory(stroke="DOG_STYLE") 
    assert any("Invalid stroke type" in err["message"] for err in chal.errors)

def test_not_in_competition_logic(db_session):
    chal = ChallengeFactory(competition_id=1)
    assert chal.not_in_competition(2) is True
    assert chal.not_in_competition(1) is False

# INTEGRATION

@pytest.mark.integration
def test_create_challenge_success(client, admin_auth_header):
    comp = CompetitionFactory()
    db.session.commit() 
    payload = {
        "name": "Morning Swim",
        "distance": 500,
        "stroke": "FREESTYLE",
        "competition_id": comp.id
    }
    response = client.post(f"/competition/{comp.id}/challenge", json=payload, headers=admin_auth_header)
    assert response.status_code == 201


@pytest.mark.integration
def test_create_challenge_invalid_data(client, admin_auth_header):
    comp = CompetitionFactory()
    db.session.commit()
    payload = {
        "name": "Broken Challenge",
        "distance": -50, 
        "stroke": "BUTTERFLY",
        "competition_id": comp.id
    }
    response = client.post(f"/competition/{comp.id}/challenge", json=payload, headers=admin_auth_header)
    assert response.status_code == 422
    assert any("Distance must be greater than zero" in err["message"] for err in response.json["errors"])


from .factories import CompetitionFactory, UserFactory
from app.model import Competition , db 
import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime , date

def test_competition_valid_model(db_session):
    comp = CompetitionFactory()
    db_session.flush()
    assert not comp.errors
    assert comp.id is not None

def test_competition_validation_earlier_date(db_session):
    comp = CompetitionFactory(date=date(1999, 12, 31))
    assert {"message": "Date cannot be earlier than 2000"} in comp.errors

def test_competition_validation_empty_name(db_session):
    comp = CompetitionFactory(name="")
    assert {"message": "Name cannot be empty"} in comp.errors

# INTEGRATION TESTS 

def test_update_competition_success(client, admin_auth_header, db_session):
    comp = CompetitionFactory(name="Old Name", location="Old City")
    db_session.commit()
    payload = {
        "competition_id": comp.id,
        "name": "New Super Name",
        "location": "New City",
        "date": "2027-01-01"
    }
    
    response = client.put("/competition/", json=payload, headers=admin_auth_header)
    assert response.status_code == 200


def test_competition_name_max_length(client, admin_auth_header, db_session):
    payload = {
        "name": "This Name Is Way Too Long For Our Database", # > 25 символів
        "location": "Kyiv",
        "date": "2026-01-01"
    }
    response = client.post("/competition/", json=payload, headers=admin_auth_header)
    assert response.status_code == 422

def test_update_competition_missing_data(client, admin_auth_header, db_session):
    comp = CompetitionFactory()
    db_session.commit()
    payload = {
        "competition_id": comp.id,
        "name": "Only Name"
    }
    response = client.put("/competition/", json=payload, headers=admin_auth_header)
    assert response.status_code == 400
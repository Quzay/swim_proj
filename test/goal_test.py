from .factories import GoalFactory, ActivityFactory
from app.model import Goal , db , User , Activity, ModelName
import pytest
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta , datetime

def test_goal_model_validation_errors(db_session):
    goal = GoalFactory(target_distance="not_int", deadline="invalid-date")
    assert "Distance must be number" in goal.errors
    assert "Deadline format must be YYYY-MM-DD" in goal.errors

def test_goal_model_negative_distance(db_session):
    goal = GoalFactory(target_distance=-100)
    assert any("Distance can not be negative" in str(e) for e in goal.errors)

def test_goal_model_past_deadline(db_session):
    goal = GoalFactory(deadline="2020-01-01")
    assert "Deadline cannot be in the past" in goal.errors


# Integration
@pytest.mark.integration
def test_create_goal_success(client, auth_header):
    payload = {
        "target_distance": 5000,
        "deadline": (date.today() + timedelta(days=30)).isoformat()
    }
    response = client.post("/goal/", json=payload, headers=auth_header)
    assert response.status_code == 200


@pytest.mark.integration
def test_create_goal_db_constraint_violation(client, auth_header):
    payload = {
        "target_distance": 0,
        "deadline": (date.today() + timedelta(days=30)).isoformat()
    }
    response = client.post("/goal/", json=payload, headers=auth_header)
    assert response.status_code == 422


@pytest.mark.integration
def test_goal_calculated_properties(client, auth_header, db_session):
    user = User.query.filter_by(email="test@gmail.com").first()
    Goal.query.filter_by(user_id=user.id).delete()
    Activity.query.filter_by(user_id=user.id).delete()
    db_session.commit()

    future_deadline = datetime.now() + timedelta(days=30)
    GoalFactory(target_distance=5000, deadline=future_deadline, user_id=user.id)
    activity = Activity(
        distance_meters=1200,
        user_id=user.id,
        stroke="FREESTYLE", 
        created_at=datetime.now(),
        time_s = 100.5 , 
        model_name = ModelName.GOAL,
        referense_id = 1
    )
    db_session.add(activity)
    db_session.commit() 
   
    response = client.get("/goal/", headers=auth_header)
    assert response.status_code == 200
    assert "3800 remained meters" in response.json["remaining_distance"]

@pytest.mark.integration
def test_show_goal_not_found(client, auth_header, db_session):
    user = User.query.filter_by(email="test@gmail.com").first()
    Goal.query.filter_by(user_id=user.id).delete()
    db_session.commit()

    response = client.get("/goal/", headers=auth_header)
    assert response.status_code == 404
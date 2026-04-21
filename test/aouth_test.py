from unittest.mock import MagicMock , patch
from app.model import User
from .factories import UserFactory
import pytest

@pytest.mark.integration
def test_facebook_auth_logic(client, db_session, mock_fb_payload):
    with patch('app.controller.oauth.oauth.facebook') as mocked_fb:
        mock_response =MagicMock()
        mock_response.json.return_value = mock_fb_payload
        mocked_fb.authorize_access_token.return_value = {"access_token": "fake"}
        mocked_fb.get.return_value = mock_response
        response = client.get("auth/facebook/auth")

        assert response.status_code == 200

@pytest.mark.integration
def test_facebook_link_to_existing_email(client, db_session, mock_fb_payload_2):
    existing_user = UserFactory(email = mock_fb_payload_2.get("email"))
    db_session.add(existing_user)
    db_session.commit()
    db_session.expunge_all() 
    db_session.close()
    with patch('app.controller.oauth.oauth.facebook') as mocked_fb:
        mock_response =MagicMock()
        mock_response.json.return_value = mock_fb_payload_2
        mocked_fb.authorize_access_token.return_value = {"access_token": "fake"}
        mocked_fb.get.return_value = mock_response
        response = client.get("/auth/facebook/auth")
        assert response.status_code == 200
        
        updated_user = User.query.filter_by(email=mock_fb_payload_2['email']).first()
        assert updated_user.facebook_id == mock_fb_payload_2['id']

@pytest.mark.integration
def test_facebook_registration_age_error(client, db_session):
    bad_fb_payload = {
        "id": "999888777",
        "name": "Little Kid",
        "email": "baby@example.com",
        "age_range": {"min": 3}  
    }
    with patch('app.controller.oauth.oauth.facebook') as mocked_fb:
        mock_response = MagicMock()
        mock_response.json.return_value = bad_fb_payload
        mocked_fb.authorize_access_token.return_value = {"access_token": "fake"}
        mocked_fb.get.return_value = mock_response
        response = client.get("/auth/facebook/auth")

        assert response.status_code == 400
        
       
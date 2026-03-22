from flask import Blueprint, jsonify , url_for 
from flask_jwt_extended import create_access_token
from app.model import User 
from app import oauth , db
import uuid
from .user_contoller import create_user_logic

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/facebook/")
def facebook():
    redirect_uri = url_for("auth.facebook_auth", _external = True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@auth_bp.route("/facebook/auth")
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get(
        'https://graph.facebook.com/me?fields=id,name,email,age_range'
    )
    profile = resp.json()
    fb_id = str(profile.get("id"))
    email = profile.get("email")

    user = User.query.filter_by(facebook_id=fb_id).first()
    if not user:
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                user.facebook_id = fb_id
                db.session.commit()
        if not user:
            fb_age = profile.get('age', 18)
            fb_data = {
                "username": profile.get('name'),
                "email": email, 
                "age": fb_age,
                "password": str(uuid.uuid4()), 
                "facebook_id": fb_id
            }
            user, errors = create_user_logic(fb_data)           
            if errors:
                return jsonify({"error": errors}), 400
    access_token = create_access_token(identity=user.email, additional_claims={"role": user.role})
    return jsonify({"access_token": access_token})
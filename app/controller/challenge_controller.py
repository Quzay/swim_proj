from flask import Blueprint, request, jsonify
from app.model import db
from app.model import Challenge
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import IntegrityError 

challenge_bp = Blueprint("challenge" , __name__)

@challenge_bp.post("/")
@jwt_required()
def create_challenge():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message":"You dont have permission"}) , 403
    data = request.get_json()
    new_chellenge = Challenge(
        name = data.get("name"),
        description = data.get("description"),
        image = data.get("image"),
        created_at = date.today(),
        expired_at = data.get("expired_at")
    )
    db.session.add(new_chellenge)
    db.session.commit()
    return jsonify({"message":"Challenge was successful created"}) , 201
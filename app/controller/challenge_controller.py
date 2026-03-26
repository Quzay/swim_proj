from flask import Blueprint, request, jsonify
from app.model import db , Challenge, User , User_challenge
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt , get_jwt_identity
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
        expired_at = data.get("expired_at"),
        distance = data.get("distance")
    )
    db.session.add(new_chellenge)
    db.session.commit()
    return jsonify({"message":"Challenge was successful created"}) , 201

@challenge_bp.post("/<int:challenge_id>")
@jwt_required()
def take_part_in_challenge(challenge_id):
    email = get_jwt_identity()
    user = User.query.filter_by(email = email).first()
    if not user:
        return jsonify({"message":"Please log in"}) , 401
    user_in_challenge = User_challenge(
        user_id = user.id,
        challenge_id = challenge_id,
        status = "ACTIVE"
    )
    db.session.add(user_in_challenge)
    db.session.commit()
    return jsonify({"message":"You take part in challenge"}) , 201

@challenge_bp.get("/") # Need to change endpoint
@jwt_required()
def show_users_active_challenge():
    email = get_jwt_identity()
    user = User.query.filter_by(email = email).first()
    if not user:
        return jsonify({"message":"Please log in"}) , 401
    active_challenge = User_challenge.query.filter_by(user_id = user.id).first()
    return jsonify({
        "id" : active_challenge.id,
        "user_id" : active_challenge.user_id,
        "challenge_id" : active_challenge.challenge_id,
        "status" : active_challenge.status,
        "current_value" : active_challenge.current_value,
        "compleated_at" : active_challenge.compleated_at
        }) , 201
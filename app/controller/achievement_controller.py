from flask import Blueprint, request, jsonify
from app.model import db , Achievement, User , user_competition_association_table , Stroke_type
from flask_jwt_extended import jwt_required, get_jwt , get_jwt_identity
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import select , exists

achievement_bp = Blueprint("achievement" , __name__)

@achievement_bp.post("/competition/<int:competition_id>/challenge/<int:challenge_id>/achievement")
@jwt_required()
def create_achievement(challenge_id,competition_id):
    user = User.find_by_email(get_jwt_identity())
    if not User:
        return jsonify({"message":"Please Log In"}), 403
    stmt = select(
        exists().where(
            user_competition_association_table.c.competition_id == competition_id,
            user_competition_association_table.c.user_id == user.id
        )
    )
    is_participant = db.session.scalar(stmt)
    if not is_participant:
        return jsonify({"message":"You arent take part in competition"}), 400 #?
    data = request.get_json()
    stroke_enum = Stroke_type[data.get("stroke").upper()]
    new_achievement = Achievement(
    stroke = stroke_enum,
    time = data.get("time"),
    distance_meters = data.get("distance"),
    user_id = user.id,
    challenge_id = challenge_id
    )
    db.session.add(new_achievement)
    db.session.commit() 
    return jsonify({"message":"You successful created an achievement"}) , 200
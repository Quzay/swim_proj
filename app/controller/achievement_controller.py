from flask import Blueprint, request, jsonify
from app.model import db , Achievement, User , user_competition_association_table , Stroke_type, Competition , Challenge, Status, Rating , ModelName
from flask_jwt_extended import jwt_required , get_jwt_identity
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import select , exists , func

achievement_bp = Blueprint("achievement" , __name__)

@achievement_bp.post("/competition/<int:competition_id>/challenge/<int:challenge_id>/achievement")
@jwt_required()
def create_achievement(challenge_id,competition_id):
    user = User.find_by_email(get_jwt_identity())
    if not User:
        return jsonify({"message":"Please Log In"}), 403
    # already_post = db.session.execute(select(Achievement).where(Achievement.challenge_id == challenge_id, Achievement.user_id == user.id)).scalar_one_or_none
    # if already_post:
    #     return jsonify({"message":"You have already posted your achievement "}), 409
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
    db.session.flush()
    competition = db.session.get(Competition, competition_id)
    exepted = competition.amount * db.session.execute(
        select(func.count())
        .select_from(Challenge)
        .where(Challenge.competition_id == competition_id)
    ).scalar()
        
    current = db.session.execute(
        select(func.count(Achievement.id))
        .join(Challenge, Achievement.challenge_id == Challenge.id)
        .where(Challenge.competition_id == competition_id)
    ).scalar() or 0
    if current >= exepted:
        competition.status = Status.COMPLETED
    challenge = db.session.get(Challenge,challenge_id)
    if data.get("distance") >= challenge.distance:
        new_rating = Rating(
            value = 5,
            user_id = user.id,
            model_name = ModelName.ACHIEVEMENT,
            referense_id = new_achievement.id
        )
        db.session.add(new_rating)
    db.session.commit() 
    return jsonify({"message":"You successful created an achievement"}) , 200
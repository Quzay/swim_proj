from datetime import datetime
from flask import Blueprint, request, jsonify
from app.model import db, Competition, Challenge, Rating, User, ModelName
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import func, select

rating_bp = Blueprint("rating" , __name__)

@rating_bp.post("/competition/<int:competition_id>/leaderboard")
def create_leaderboard(competition_id):
    competition = db.session.get(Competition, competition_id)
    if not competition:
        return jsonify({"message":"competition not found"}) , 404
    challenges = db.session.execute(select(Challenge).where(Challenge.competition_id==competition_id)).scalars().all()
    for challenge in challenges:
        bonus = 3
        top_achievements = db.session.execute(select(Achievement).
                                         where(Achievement.challenge_id == challenge.id)
                                         .order_by(Achievement.time.asc())
                                         .limit(3)
                                         ).scalars().all()
        for achievement in top_achievements:
            rating = db.session.execute(select(Rating)
                                        .where(Rating.model_name == ModelName.ACHIEVEMENT, 
                                               Rating.referense_id == achievement.id)
                                               ).scalar_one_or_none()
            if rating:
                rating.value += bonus
                bonus -= 1
            if bonus <= 0:
                break
    db.session.commit()
    return jsonify({"message":"Rating successful created"}), 200

@rating_bp.get("/competition/<int:competition_id>/leaderboard")
def show_compet_leaderboard(competition_id):
    competition = db.session.get(Competition, competition_id)
    if not competition:
        return jsonify({"message":"Competition not found"}) , 404
    ratings = db.session.execute(select(Rating.user_id, func.sum(Rating.value).label("total_score"))
                                .join(Achievement,(Rating.model_name == ModelName.ACHIEVEMENT) & (Rating.referense_id == Achievement.id) )
                                .join(Challenge, Challenge.id == Achievement.challenge_id)
                                .where(Challenge.competition_id == competition_id)
                                .group_by(Rating.user_id)
                                .order_by(func.sum(Rating.value).desc())
                                ).all()
    res = []
    place = 1
    for rating in ratings:
        user = db.session.get(User, rating.user_id)
        res.append({
            "username" : user.username,
            "total_score" : rating.total_score,
            "place":place,
            "email": user.email,
            "user_id" : user.id
        })
        place = place + 1
    return jsonify({"Competition":competition.name,
                    "leaderboard": res}) , 200

@rating_bp.get("/competition/<int:competition_id>/challenge/<int:challenge_id>/leaderboard")
def show_challenge_leaderboard(competition_id, challenge_id):
    ratings = db.session.execute(select(Rating)
                                .join(Achievement, Rating.achievement_id ==Achievement.id)
                                .where(Achievement.challenge_id  == challenge_id)
                                .order_by(Rating.value.desc())
                                ).scalars().all()
    res = []
    place = 1
    for rating in ratings:
        user = db.session.get(User, rating.user_id)
        res.append({
            "value" : rating.value,
            "username " : user.username,
            "place": place,
            "email": user.email,
            "user_id" : user.id
        })
        place = place + 1
    return jsonify(res) , 200

@rating_bp.get("/leaderboard")
def show_general_leaberboard():
    query = (
        db.session.query(User.id,User.username,func.sum(Rating.value).label("total_score"))
                        .join(Rating, User.id == Rating.user_id)
                        .group_by(User.id, User.username)
                        .order_by(func.sum(Rating.value).desc())
    )                           
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=3, type=int)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    res = []
    current_place = (page - 1) * per_page + 1
    
    for item in pagination.items:
        res.append({
            "user_id": item[0],       
            "username": item[1],      
            "value": int(item[2]) if item[2] is not None else 0, 
            "place": current_place
        }) 
        current_place += 1
    return jsonify(res), 200

@rating_bp.get("/activity/leaderboard") 
def show_activity_leaderboard():
    pass
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.model import db, Competition, Challenge, Rating, User, ModelName, Activity
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import func, select
from decimal import Decimal, ROUND_HALF_UP

rating_bp = Blueprint("rating" , __name__)

#? Хз що з цим робити
# @rating_bp.post("/competition/<int:competition_id>/leaderboard")
# def create_leaderboard(competition_id):
#     competition = db.session.get(Competition, competition_id)
#     if not competition:
#         return jsonify({"message":"competition not found"}) , 404
#     challenges = db.session.execute(select(Challenge).where(Challenge.competition_id==competition_id)).scalars().all()
#     for challenge in challenges:
#         bonus = 3
#         top_activities = db.session.execute(select(Activity).
#                                          where(Activity.referense_id == challenge.id , Activity.model_name == ModelName.CHALLENGE)
#                                          .order_by(Activity.time_s.asc())
#                                          .limit(3)
#                                          ).scalars().all()
#         for achievement in top_activities:
#             rating = db.session.execute(select(Rating)
#                                         .where(Rating.activity_id == ModelName.ACHIEVEMENT)
#                                         ).scalar_one_or_none()
#             if rating:
#                 rating.value += bonus
#                 bonus -= 1
#             if bonus <= 0:
#                 break
#     db.session.commit()
#     return jsonify({"message":"Rating successful created"}), 200

@rating_bp.get("/competition/<int:competition_id>/leaderboard")
def show_compet_leaderboard(competition_id):
    competition = db.session.get(Competition, competition_id)
    if not competition:
        return jsonify({"message":"Competition not found"}) , 404
    ratings = db.session.execute(select(Rating.user_id, func.sum(Rating.value).label("total_score"))
                                .join(Activity,(Rating.activity_id == Activity.id))
                                .join(Challenge, (Challenge.id == Activity.referense_id) & (Activity.model_name == ModelName.CHALLENGE))
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
                                .join(Activity, Rating.activity_id ==Activity.id)
                                .where(Activity.referense_id  == challenge_id, Activity.model_name == ModelName.CHALLENGE)
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

# @rating_bp.get("/leaderboard")
# def show_general_leaberboard():
#     query = (
#         db.session.query(User.id,User.username,func.sum(Rating.value).label("total_score"),func.sum(Activity.distance_meters).label("total_distance"), func.count(Activity.id))
#                         .join(Rating, User.id == Rating.user_id)
#                         .group_by(User.id, User.username)
#                         .order_by(func.sum(Rating.value).desc())
#     )                           
#     page = request.args.get("page", default=1, type=int)
#     per_page = request.args.get("per_page", default=3, type=int)
#     pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
#     res = []
#     current_place = (page - 1) * per_page + 1
    
#     for item in pagination.items:
#         if item[3] and item[3] != 0:
#             total_distance = Decimal(str(item.total_distance / 1000)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
#         else:
#             total_distance = 0
#         res.append({
#             "user_id": item[0],       
#             "username": item[1],      
#             "value": int(item[2]) if item[2] is not None else 0, 
#             "place": current_place,
#             "total_distance" : f"{total_distance} km",
#             "activity_count" : int(item[4]) if item[4] is not None else 0, 
#         }) 
#         current_place += 1
#     return jsonify(res), 200
@rating_bp.get("/leaderboard")
def show_general_leaberboard():
    stmt = (select(User).order_by(User.total_rating.desc().nulls_last()).where(User.total_distance >= 0.01))

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=3, type=int)
    pagination = db.paginate(stmt, page=page, per_page=per_page, error_out=False)
    
    res = []
    current_place = (page - 1) * per_page + 1
    
    for item in pagination.items:
                
        raw_dist = item.total_distance or 0
        total_score = item.total_rating or 0
        rating_rounded = Decimal(str(total_score)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        dist_km = Decimal(str(raw_dist / 1000)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        res.append({
            "user_id": item.id,       
            "username": item.username,      
            "value": rating_rounded, 
            "place": current_place,
            "total_distance": f"{dist_km} km",
            "activity_count": int(item.activity_count or 0), 
        }) 
        current_place += 1
        
    return jsonify(res), 200

@rating_bp.get("/activity/leaderboard") 
def show_activity_leaderboard():
    pass
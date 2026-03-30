from flask import Blueprint, request, jsonify
from app.model import db , Challenge, User 
from flask_jwt_extended import jwt_required, get_jwt , get_jwt_identity
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import select

challenge_bp = Blueprint("challenge" , __name__)

@challenge_bp.post("/competition/<int:competition_id>/challenge")
@jwt_required()
def create_challenge(competition_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message":"You dont have permission"}) , 403
    data = request.get_json()
    new_chellenge = Challenge(
        name = data.get("name"),
        description = data.get("description"),
        distance = data.get("distance"),
        competition_id = competition_id
    )
    db.session.add(new_chellenge)
    db.session.commit()
    return jsonify({"message":"Challenge was successful created"}) , 201


@challenge_bp.get("/competition/<int:competition_id>/challenges/") 
@jwt_required()
def show_all_challenges(competition_id):
    user = User.find_by_email(get_jwt_identity()) # Чи треба взагалі?
    if not user:
        return jsonify({"message":"Please log in"}) , 401
    stmt = select(Challenge).where(Challenge.competition_id == competition_id)
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page" , default=3, type=int)
    pagination = db.paginate(stmt, page = page,per_page= per_page, error_out=False)
    res = []
    for challenge in pagination:
        res.append({
            "id" : challenge.id,
            "name" : challenge.name,
            "description": challenge.description,
            "distance": challenge.distance,
            "competition_id" : challenge.competition_id
        })
    return jsonify(res), 200
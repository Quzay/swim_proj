from flask import Blueprint, request, jsonify
from app.model import db , Challenge, User , Stroke_type
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
    stroke_str = data.get("stroke")
    if stroke_str not in Stroke_type.__members__:
        return jsonify({"message": f"Invalid stroke. Choose from: {list(Stroke_type.__members__.keys())}"}), 422
    stroke_enum = Stroke_type[stroke_str.upper()]
    new_chellenge = Challenge(
        name = data.get("name"),
        description = data.get("description"),
        distance = data.get("distance"),
        competition_id = competition_id,
        stroke = stroke_enum
    )
    if new_chellenge.errors:
        return jsonify({"errors": new_chellenge.errors}), 422
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

@challenge_bp.put("/competition/<int:competition_id>/challenge/<int:challenge_id>")
@jwt_required()
def update_challenge(competition_id, challenge_id):
    user = User.find_by_email(get_jwt_identity()) # Чи треба взагалі?
    if not user:
        return jsonify({"message":"Please log in"}) , 401
    challenge = db.session.get(Challenge,challenge_id)
    if not challenge :
        return jsonify({"message":"Challenge not found"}), 404
    
    if challenge.not_in_competition(competition_id):
        return jsonify({"message":"competition doesnt have this challenge"}) , 400
    data = request.get_json()
    required_fields = ["name", "distance", "description"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": "Missing data",
            "message": f"Fields required: {', '.join(missing_fields)}"}), 422
    challenge.name = data.get("name")
    challenge.distance = data.get("distance")
    challenge.description = data.get("description")

    db.session.commit()
    return jsonify({"message":"challenge successful updated"}), 200

@challenge_bp.delete("/competition/<int:competition_id>/challenge/<int:challenge_id>")
@jwt_required()
def delete_challenge(competition_id, challenge_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message":"You dont have permission"}) , 403
    challenge = db.session.get(Challenge,challenge_id)
    if not challenge :
        return jsonify({"message":"Challenge not found"}), 404
    if competition_id != challenge.competition_id:
        return jsonify({"message":"competition doesnt have this challenge "}),400
    db.session.delete(challenge)
    db.session.commit()
    return jsonify({"message":"Challenge was successful deleted"}) , 200
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.model import db, Competition, User, user_competition_association_table
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import func, select

competition_bp = Blueprint('competition' , __name__)

@competition_bp.route("/" , methods = ["POST"])
@jwt_required()
def create_competition():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message":"You dont have permission"}) , 403
    data = request.get_json()
    # try:
    #     day_str = data.get("date")
    #     day_date = datetime.strptime(day_str, "%Y-%m-%d").date() if day_str else None
    # except (ValueError, TypeError):
    #     return jsonify({ "message":"Invalid date format. Use YYYY-MM-DD"}), 422
    new_competition = Competition(
        name = data.get("name"),
        location = data.get("location"),
        date = data.get("date"),
        amount = data.get("amount")
    )
    if new_competition.errors:
        return jsonify({"errors":new_competition.errors}), 422
    try:
        db.session.add(new_competition)
        db.session.commit()
        return jsonify ({"message":"Competition was succesful created"}) , 200
    except ValueError as e:
        db.session.rollback()
        new_competition.errors.append({"message": str(e)})
    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig)
        if "ck_competition_name" in error_msg:
            new_competition.errors.append({"message":"Name cannot be empty"})
        if "ck_competition_location" in error_msg:
            new_competition.errors.append({"message":"Location cannot be empty"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":"An unexpected error occurred"}) , 500
    if new_competition.errors:
        return jsonify({"errors":new_competition.errors}) , 422

@competition_bp.post("<int:competition_id>/join/") #? maybe change this
@jwt_required()
def join_competition(competition_id):
    user = User.find_by_email(get_jwt_identity())
    if not user:
        return jsonify({"message":"Plase Log In"}) , 401
    competition = Competition.query.get(competition_id)
    if not competition:
        return jsonify({"message":"Competition not found"}) , 404
    current_count = db.session.execute(select(func.count()).where(
        user_competition_association_table.c.competition_id == competition.id)).scalar() or 0
    if competition.is_open:
        if user not in competition.users:
            competition.users.append(user)
            if current_count + 1 >= competition.amount:
                competition.is_open = False
            db.session.commit()
            return jsonify({"message":"You successful registred"}) , 200
        else:
            return jsonify({"message":"You already register"}) , 409
    else:
        return jsonify({"message":"No places left or competition is over"}) , 400 #?

@competition_bp.route("/" , methods = ["GET"])
def show_competition():
    competition = Competition.query.all()
    if not competition:
        return jsonify({"message":"Competitions not found"}) ,404
    
    ret = []
    for compet in competition:
        current_count = db.session.execute(select(func.count())
                                           .where(user_competition_association_table.c.competition_id == compet.id)
                                           ).scalar() or 0
        ret.append({
            "name" : compet.name,
            "location" : compet.location,
            "date" : compet.date,
            "registered" : current_count,
            "amount" : compet.amount,
            "is_open" : compet.is_open,
            "status": compet.status,
            "id" : compet.id
        })
    return jsonify(ret) , 200

@competition_bp.route("/" , methods = ["DELETE"])
@jwt_required()
def delete_competition():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message":"You dont have permission"}) , 403
    data = request.get_json()
    compet_id = data.get("competition_id")
    if not compet_id:
        return jsonify({"message":"Need Competition ID to delete" }) , 404
    competition = Competition.query.get(compet_id)
    if not competition:
        return jsonify({"message":"Competition not found"}), 404
    db.session.delete(competition)
    db.session.commit()
    return jsonify({"message":"Competition was successful deleted"}) , 200

@competition_bp.route("/" , methods = ["PUT"])
@jwt_required()
def change_competition():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message":"You dont have permission"}) , 403
    data = request.get_json()
    compet_id = data.get("competition_id")
    if not compet_id:
        return jsonify({"message":"Need Competition ID to change"}), 404
    competition = Competition.query.get(compet_id)
    if not competition:
        return jsonify({"message":"Competition not found"}) , 404
    required_fields = ["name" , "location" , "date"]
    missing_field = [field for field in required_fields if field not in data]
    if missing_field:
        return jsonify({"message":"Missing data"}) , 400
    day_str = data.get("date")
    day_date = datetime.strptime(day_str, "%Y-%m-%d").date()
    competition.name = data.get("name")
    competition.location = data.get("location")
    competition.date = day_date
    db.session.commit()
    return jsonify({"message":"Competition was successful changed"}) , 200


from datetime import datetime
from flask import Blueprint, request, jsonify
from app.model import db, Competition

competition_bp = Blueprint('competition' , __name__)

@competition_bp.route("/" , methods = ["POST"])
def create_competition():
    data = request.get_json()
    day_str = data.get("date")
    day_date = datetime.strptime(day_str, "%Y-%m-%d").date()
    new_competition = Competition(
        name = data.get("name"),
        location = data.get("location"),
        date = day_date
    )
    db.session.add(new_competition)
    db.session.commit()
    return jsonify ({"message":"Competition was succesful created"}) , 200

@competition_bp.route("/" , methods = ["GET"])
def show_competition():
    competition = Competition.query.all()
    if not competition:
        return jsonify({"message":"Competitions not found"}) ,404
    ret = []
    for compet in competition:
        ret.append({
            "name" : compet.name,
            "location" : compet.location,
            "date" : compet.date
        })
    return jsonify(ret) , 200

@competition_bp.route("/" , methods = ["DELETE"])
def delete_competition():
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
def change_competition():
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
    competition.name = data.get("name")
    competition.location = data.get("location")
    competition.date = data.get("date")
    db.session.commit()
    return jsonify({"message":"Competition was successful changed"}) , 200

@competition_bp.route("/" , methods = ["PATCH"])
def update_competition():
    data = request.get_json()
    compet_id = data.get("competition_id")
    if not compet_id:
        return jsonify({"message":"Need Competition ID to change"}), 404
    competition = Competition.query.get(compet_id)
    if not competition:
        return jsonify({"message":"Competition not found"}) , 404
    if "name" in data:
        competition.name = data.get("name")
    if "location" in data:
        competition.location = data.get("location")
    if "date" in data:
        competition.date = data.get("date")
    db.session.commit()
    return jsonify({"message":"Competition was successful updated"}) , 200
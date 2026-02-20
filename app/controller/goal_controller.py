from flask import Blueprint, request, jsonify
from app.model import db, User, Goal
from datetime import datetime,date
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError 


goal_bp = Blueprint('goal' , __name__)

@goal_bp.route("/<int:user_id>" , methods = ["POST"])
def add_goal(user_id):
    user = User.query.get(user_id)
    if not user :
        return jsonify({"message " : "User not found"}),404
    data = request.get_json()
    try:
        new_goal = Goal(
        target_distance  = data.get("target_distance"),
        deadline = data.get("deadline"),
        user_id = user_id
        )
        db.session.add(new_goal)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig)
        if "ck_goal_targer_distance" in error_msg:
            return jsonify({"message":"Distance cannot be negative"}), 400
        if "ck_goal_deadline" in error_msg:
            return jsonify({"message":"deadline cannot be empty"}) , 400
    except ValueError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}) , 400
    except Exception as e:
        db.session.rollback()
        print()
        return jsonify({"message":"An unexpected error occurred",
                        "ПОМИЛКА ТУТ": {type(e).__name__} - {e}}) , 500
    return jsonify({"message " : "Goal was successful created"}) , 200

@goal_bp.route("/<int:user_id>" , methods = ["GET"])
def show_goal(user_id):
    goal = Goal.query.filter_by(user_id=user_id).order_by(desc(Goal.id)).first()
    if not goal:
        return jsonify({"You don't have goal"}), 404
    return jsonify({
        "id" : goal.id,
        "distance" : f"{goal.target_distance} meters",
        "deadline" : goal.deadline ,
        "remaining_distance" : f"{goal.remaining_distance} remained meters",
        "days_left" : f"{goal.days_left} day"
    }) , 200

@goal_bp.route("/<int:user_id>" , methods = ["DELETE"])
def delete_goal(user_id):
    data = request.get_json()
    goal_id = data.get("goal_id")
    if not goal_id : 
        return jsonify ({"message":"Goal ID is required"}) , 400
    goal = Goal.query.filter_by(id = goal_id, user_id = user_id).first()
    if not goal:
        return jsonify ({"message":"Goal not found or access denied"}) , 404
    db.session.delete(goal)
    db.session.commit()
    return jsonify ({"message":"Goal was succesful deleted"}) , 200

@goal_bp.route("/<int:user_id>" , methods = ["PUT"])
def change_goal(user_id):
    data = request.get_json()
    goal_id = data.get("goal_id")
    if not goal_id:
        return jsonify({"message":"Goal ID is required"}) , 400
    goal = Goal.query.filter_by(id=goal_id, user_id = user_id).first()
    if not goal:
        return jsonify({"message":"Goal not found or access denied"}), 404
    required_fields = ["target_distance" , "deadline"]
    missing_field = [field for field in required_fields if field not in data]
    if missing_field:
        return jsonify({"message":"Missing data"}) , 400
    goal.target_distance = data.get("target_distance")
    goal.deadline = date.fromisoformat(data.get("deadline"))
    db.session.commit()
    return jsonify({"message":"Goal was successful changed"}), 200

@goal_bp.route("/<int:user_id>" , methods = ["PATCH"])
def update_goal(user_id):
    data = request.get_json()
    goal_id = data.get("goal_id")
    if not goal_id:
        return jsonify({"message":"Goal ID is required"}) , 400
    goal = Goal.query.filter_by(id=goal_id,user_id=user_id).first()
    if not goal:
        return jsonify({"message":"Goal not found or access denied"}), 404
    if "deadline" in data:
        goal.deadline = date.fromisoformat(data.get("deadline"))
    if "target_distance" in data:
        goal.target_distance = data.get("target_distance")
    db.session.commit()
    return jsonify({"message":"Goal was successful changed"}) , 200
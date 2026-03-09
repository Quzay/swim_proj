from flask import Blueprint, request, jsonify
from app.model import db
from app.model import User, Activity , Stroke_type
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError 

activity_bp = Blueprint('activity', __name__)

@activity_bp.route("/", methods=["POST"])
@jwt_required()
def create_activity():
    data = request.get_json()
    email = get_jwt_identity()
    user = User.query.filter_by(email = email).first()
    if not user:
        return jsonify({"message" : "User not found"}) , 404
    
    stroke_str = data.get("stroke")
    if stroke_str not in Stroke_type.__members__:
        return jsonify({"message": f"Invalid stroke. Choose from: {list(Stroke_type.__members__.keys())}"}), 422
    stroke_enum = Stroke_type[stroke_str.upper()]
    try:
        new_activity = Activity(
        stroke = stroke_enum,
        distance_meters = data.get("distance_meters"),
        user_id = user.id
        )
        db.session.add(new_activity)
        db.session.commit()
        return jsonify({"message" : "Activity was succesful created"}), 200
    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig)
        if "ck_activity_distance" in error_msg:
            new_activity.errors.append({"message":"Distance cannot be negative"})

        if new_activity.errors:
            return jsonify(new_activity.errors) , 422
    except ValueError as e:
        db.session.rollback()
        new_activity.errors.append({"message":str(e)})
    except Exception as e:
        db.session.rollback()
        new_activity.errors.append([{"message": f"Server error: {str(e)}"}])
        if new_activity.errors:
            return jsonify(new_activity.errors)

@activity_bp.route("/<int:user_id>" , methods = ["PATCH"])
def update_activity(user_id):
    data = request.get_json()
    activity_id = data.get("activity_id")
    activity = Activity.query.filter_by(id = activity_id, user_id = user_id).first()
    if not activity:
        return jsonify ({"message":"Activity not found or access denied"}) , 404
    
    if "stroke" in data:
        stroke_enum = Stroke_type[data.get("stroke").upper()]
        activity.stroke = stroke_enum
    if "distance_meters" in data:
        activity.distance_meters = data.get("distance_meters")
    if "day" in data:
        activity.day = datetime.fromisoformat(data.get("day"))
    db.session.commit()
    return jsonify ({"message" : "Activity was succesful update"}) , 200

@activity_bp.route("/<int:user_id>" , methods = ["DELETE"])
def delete_activity(user_id):
    data = request.get_json()
    activity_id = data.get("activity_id")
    activity = Activity.query.filter_by(id = activity_id, user_id = user_id).first()
    if not activity:
        return jsonify ({"message":"Activity not found or access denied"}) , 404
    db.session.delete(activity)
    db.session.commit()
    return jsonify({"message" : "Activity was succesful deleted"}), 200

@activity_bp.route("/<int:user_id>" , methods = ["GET"])
def show(user_id):
    activity = Activity.get_all_activity_by_user(user_id)
    if not activity:
        return jsonify({"message" : "Activity not found"}) , 404
    ret = []
    for act in activity:
        ret.append({
            "id" : act.id,
            "stroke": act.stroke.value,
            "distance_meters" : act.distance_meters,
            "day" : act.day.isoformat()
        })
    return jsonify(ret) , 200

@activity_bp.route("/<int:user_id>" , methods = ["PUT"])
def change_last_activity(user_id):
    data = request.get_json()
    activity_id = data.get("activity_id")
    activity = Activity.query.filter_by(id = activity_id, user_id = user_id).first()
    if not activity:
        return jsonify ({"message":"Activity not found or access denied"}) , 404
    required_fields = ["stroke" , "distance_meters" , "day"]
    missing_field = [field for field in required_fields if field not in data]
    if missing_field:
        return jsonify({"message" : "Missing data"}) , 400
    stroke_enum = stroke_enum = Stroke_type[data.get("stroke").upper()]
    activity.stroke = stroke_enum
    activity.disctance_meters = data.get("distance_meters")
    activity.day = datetime.fromisoformat(data.get("day"))
    db.session.commit()
    return jsonify({"message" : "Activity was successful changed"}) , 200



# @activity_bp.route("/del/<int:activity_id>" , methods = ["DELETE"])
# def del_activity(activity_id):
#     activity = Activity.query.get(activity_id)
#     if not activity:
#         return jsonify ({"message" : "Activity not found"}) , 404
#     db.session.delete(activity)
#     db.session.commit()
#     return jsonify ({"message" : "Activity was successful deleted"}) , 200

# @activity_bp.route("/show/<int:activity_id>" , methods = ["GET"])
# def show_activity(activity_id):
#     activity = Activity.query.get(activity_id)
#     if not activity: 
#         return jsonify ({"message " : "Activity not found"}) , 404
#     return jsonify({
#         "stroke" : activity.stroke.value,
#         "distance_meters" : activity.distance_meters,
#         "day" : activity.day.isoformat()
#     }) , 200

# @activity_bp.route("/up/<int:activity_id>" , methods = ["PATCH"])
# def up_activity(activity_id):
#     activity = Activity.query.get(activity_id)
#     if not activity: 
#         return jsonify ({"message " : "Activity not found"}) , 404
#     data = request.get_json()
#     if "stroke" in data:
#         activity.stroke = data["stroke"]
#     if "distance_meters" in data:
#         activity.distance_meters = data["distance_meters"]
#     if "day" in data:
#         activity.day = data["day"]
#     db.session.commit()
#     return jsonify({"message" : "Activity was updated"}) , 200
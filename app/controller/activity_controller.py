from flask import Blueprint, request, jsonify
from app.model import db
from app.model import User, Activity


activity_bp = Blueprint('activity', __name__)

@activity_bp.route("/add/<int:user_id>", methods=["POST"])
def create_activity(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message" : "User not found"})
    else:
        new_activity = Activity(
        stroke = data.get("stroke"),
        distance_meters = data.get("distance_meters"),
        user_id = user_id
        )
    db.session.add(new_activity)
    db.session.commit()
    return jsonify({"message" : "Activity was succesful created"}), 200

@activity_bp.route("/update/<int:user_id>" , methods = ["PATCH"])
def update_activity(user_id):
    activity = Activity.get_last_by_user_id(user_id)
    if not activity:
        return jsonify ({"message" : "Activity nof found"}), 404
    data = request.get_json()
    
    if "stroke" in data:
        activity.stroke = data["stroke"]
    if "distance_meters" in data:
        activity.distance_meters = data["distance_meters"]
    if "day" in data:
        activity.day = data["day"]
    db.session.commit()
    return jsonify ({"message" : "Activity was succesful update"}) , 200

@activity_bp.route("/delete/<int:user_id>" , methods = ["DELETE"])
def delete_activity(user_id):
    activity = Activity.get_last_by_user_id(user_id)
    if not activity:
        return jsonify({"message" : "Activity not found"}), 404
    db.session.delete(activity)
    db.session.commit()
    return jsonify({"message" : "Activity was succesful deleted"}), 200

@activity_bp.route("/show-last-activity/<int:user_id>" , methods = ["GET"])
def show(user_id):
    activity = Activity.get_last_by_user_id(user_id)
    if not activity:
        return jsonify({"message" : "Activity not found"}) , 404
    user = User.query.get(user_id)
    return jsonify ({
        "There is last activity": f"from user {user.username}",
        "stroke ": activity.stroke,
        "distance_meters" : activity.distance_meters,
        "day" : activity.day
    })
@activity_bp.route("/change-last-activity/<int:user_id>" , methods = ["PUT"])
def change_last_activity(user_id):
    activity = Activity.get_last_by_user_id(user_id)
    if not activity:
        return jsonify({"message" : "Activity not found"}) , 404
    data = request.get_json()
    required_fields = ["stroke" , "distance_meters" , "day"]
    missing_field = [field for field in required_fields if field not in data]
    if missing_field:
        return jsonify({"message" : "Missing data"})
    activity.stroke = data["stroke"]
    activity.disctance_meters = data["distance_meters"]
    activity.day = data["day"]
    db.session.commit()
    return jsonify({"message" : "Activity was successful changed"}) , 200



@activity_bp.route("/del/<int:activity_id>" , methods = ["DELETE"])
def del_activity(activity_id):
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify ({"message" : "Activity not found"}) , 404
    db.session.delete(activity)
    db.session.commit()
    return jsonify ({"message" : "Activity was successful deleted"}) , 200

@activity_bp.route("/show/<int:activity_id>" , methods = ["GET"])
def show_activity(activity_id):
    activity = Activity.query.get(activity_id)
    if not activity: 
        return jsonify ({"message " : "Activity not found"}) , 404
    return jsonify({
        "stroke" : activity.stroke,
        "distance_meters" : activity.distance_meters,
        "day" : activity.day
    }) , 200

@activity_bp.route("/up/<int:activity_id>" , methods = ["PATCH"])
def up_activity(activity_id):
    activity = Activity.query.get(activity_id)
    if not activity: 
        return jsonify ({"message " : "Activity not found"}) , 404
    data = request.get_json()
    if "stroke" in data:
        activity.stroke = data["stroke"]
    if "distance_meters" in data:
        activity.distance_meters = data["distance_meters"]
    if "day" in data:
        activity.day = data["day"]
    db.session.commit()
    return jsonify({"message" : "Activity was updated"}) , 200
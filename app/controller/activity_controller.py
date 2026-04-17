from flask import Blueprint, request, jsonify
from app.model import db
from app.model import User, Activity , Stroke_type , Goal , Status , Rating , ModelName , Challenge, Competition
from datetime import datetime , date
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import select

activity_bp = Blueprint('activity', __name__)

@activity_bp.post("/competition/<int:competition_id>/challenge/<int:challenge_id>/activity")
@jwt_required()
def create_challennge_activity(competition_id, challenge_id):
    user = User.find_by_email(get_jwt_identity())
    if not user:
        return jsonify({"message" : "Please Log In"}) , 401
    competition = db.session.get(Competition, competition_id)
    challenge = db.session.get(Challenge, challenge_id)
    if not competition:
        return jsonify({"message":"Competition not found"}), 404
    if not challenge:
        return jsonify({"message" : "Challenge not found"}), 404
    if challenge.competition_id != competition_id:
        return jsonify({"message" : "Competition doesn't have this challenge"}) , 400
    if not Competition.check_participate(competition_id, user.id):
        return jsonify({"message" : "You don't take part in competition"}), 400
    if Competition.status == Status.COMPLETED:
        return jsonify({"message" : "Competition is over"}) , 400
    if Activity.already_post(challenge_id, user.id):
        return jsonify({"message":"You already post activity to this challenge"}) , 400
    data = request.get_json()
    stroke_str = data.get("stroke")
    if stroke_str not in Stroke_type.__members__:
        return jsonify({"message": f"Invalid stroke. Choose from: {list(Stroke_type.__members__.keys())}"}), 422
    stroke_enum = Stroke_type[stroke_str.upper()]
    try:
        new_activity = Activity(
            stroke = stroke_enum,
            distance_meters = data.get("distance_meters"),
            user_id = user.id,
            time_s = data.get("time_s"),
            referense_id = challenge_id,
            model_name = ModelName.CHALLENGE,
        )
        db.session.add(new_activity)
        db.session.flush()
        # user_goal = Goal.query.filter_by(user_id=user.id).first()
        # if user_goal:
        #     if user_goal.status == Status.ACTIVE:
        #         db.session.refresh(user_goal)
        #         if user_goal.remaining_distance <= 0:
        #             user_goal.status = Status["COMPLETED"]
        #             user_goal.deadline = date.today()
        new_activity.check_require(challenge_id)
        if competition.check_number_of_free_activity():
                db.session.commit()
                return jsonify({"message":"Activity was succesful created and Winners have been determined"}), 200
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

@activity_bp.get('/activity/')


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

@activity_bp.get("/activity/<int:activity_id>")
def show_activity(activity_id):
    activity = db.session.get(Activity, activity_id)
    if not activity:
        return jsonify({"message" : "Activity not found"}) , 404
    rating = db.session.scalar(select(Rating.value).where(Rating.activity_id == activity.id))
    return jsonify({"id" : activity.id,
            "stroke": activity.stroke.value,
            "distance_meters" : activity.distance_meters,
            "created_at" : activity.created_at.isoformat(),
            "speed" : f"{activity.speed} meters/second",
            "model_name" : activity.model_name.value,
            "refernse_id" : activity.referense_id,
            "rating" : rating,
            "time_s" : activity.time_s
        })
    

@activity_bp.get("/activities")
@jwt_required()
def show_all_activities():
    user = User.find_by_email(get_jwt_identity())
    activity = Activity.get_all_activity_by_user(user.id)
    if not activity:
        return jsonify({"message" : "Activity not found"}) , 404
    ret = []
    for act in activity:
        rating = db.session.scalar(select(Rating.value).where(Rating.activity_id == act.id))
        ret.append({
            "id" : act.id,
            "stroke": act.stroke.value,
            "distance_meters" : act.distance_meters,
            "created_at" : act.created_at.isoformat(),
            "speed" : f"{act.speed} meters/second",
            "model_name" : act.model_name.value,
            "refernse_id" : act.referense_id,
            "rating" : rating,
            "time_s" : act.time_s
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


from flask import Blueprint, request, jsonify
from app.model import db, User , Equipment, Equipment_type , Activity , Rating
from sqlalchemy.exc import IntegrityError 
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select, func

equipment_bp = Blueprint("equipment" , __name__)

@equipment_bp.post("/activity/<int:activity_id>/equipment")
@jwt_required()
def create_equipment(activity_id):
    user = User.find_by_email(get_jwt_identity())
    activity = db.session.get(Activity, activity_id)
    if activity.user_id != user.id :
        return jsonify({"message":"This activity is not yours"}) , 403
    data = request.get_json()
    type_str = data.get("type")
    if type_str not in Equipment_type.__members__:
        return jsonify({"message": f"Invalid Equipment. Choose from: {list(Equipment_type.__members__.keys())}"}), 422
    type_enum = Equipment_type[type_str.upper()]
    new_equipment = Equipment(
        name = data.get("name"),
        brand = data.get("brand"),
        activity_id = activity_id,
        type = type_enum
    )
    db.session.add(new_equipment)
    db.session.commit()
    return jsonify({"message":"You successful added equipment"}) , 200

@equipment_bp.put("/activity/<int:activity_id>/equipment/<int:equipment_id>")
@jwt_required()
def break_equipment(activity_id, equipment_id):
    user = User.find_by_email(get_jwt_identity())
    activity = db.session.get(Activity, activity_id)
    if not activity: 
        return jsonify({"message":"Activity not found"}), 404
    equipment = db.session.get(Equipment, equipment_id)
    if activity.id != equipment.activity_id:
        return jsonify({"message":"That equipment not from this activity"}) , 400
    if user.id != activity.user_id:
        return jsonify({"message":"That is not your equipment"}) , 403
    if equipment.is_broken == False :
        equipment.is_broken = True
    else:
        return jsonify ({"message":"You already break this equipment"}) , 400
    rating = db.session.scalar(select(Rating).where(Rating.activity_id == activity_id))
    rating.value -=2
    rating.updated_at = func.now() 
    db.session.commit()
    return jsonify({"message":"You , unfortunately, break the equipment "}) , 200

@equipment_bp.get("/activity/<int:activity_id>/equipment")
def show_equipment(activity_id):
    equipment = db.session.scalar(select(Equipment).where(Equipment.activity_id == activity_id))
    if not equipment:
        return jsonify({"message":"Equipment not found"}) , 404
    return jsonify({
        "name": equipment.name,
        "brand" : equipment.brand,
        "type" : equipment.type,
        "activity_id" : equipment.activity_id,
        "is_broken" : equipment.is_broken
        }) , 200
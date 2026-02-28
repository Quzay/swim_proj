from flask import Blueprint, request , jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.model import User

users_bp = Blueprint("users", __name__)

@users_bp.get("/")
@jwt_required()
def get_all_users():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message":"You dont have permission"}) , 403
    page = request.args.get("page", default=1, type=int)
    pagination = User.query.paginate(page = page,per_page= 10, error_out=False)
    if not pagination or pagination == None:
        return jsonify({"message":"No users registred"})
    res = []
    for user in pagination:
        res.append({
            "id" : user.id,
            "username" : user.username,
            "email": user.email,
            "age": user.age,
            "created_at" : user.created_at
        })
    return jsonify(res), 200
    
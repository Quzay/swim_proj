from app.model import db
from flask import request, jsonify, Blueprint
from app.model import User


user_bp = Blueprint('user', __name__)

@user_bp.route("/add" , methods = ["POST"])
def add_user():
    if request.method == "POST":
        data = request.get_json()
        new_user = User(
            username = data.get("username"),
            email = data.get("email"),
            age = data.get("age")
        )
        password_from_data = data.get("password")
        if password_from_data:
            new_user.set_password(password_from_data)
        else:
            return jsonify({"message": "Password is required"}), 400
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added successfully"}), 201

@user_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if request.method == "DELETE":
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        data = request.get_json()
        email_val = data.get("email")
        password_val = data.get("password")
        user = db.session.execute(db.select(User).filter_by(email=email_val)).scalar_one_or_none()
        
        if user and user.check_password(password_val):
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"}), 200
        return jsonify({"message": "Invalid email or password"}), 401

@user_bp.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    data = request.get_json()
    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "age" in data:
        user.age = data["age"]
    if "password" in data:
        user.set_password(data["password"])
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

@user_bp.route('/get/<int:user_id>' , methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "created_at": user.created_at.isoformat()
    }
    return jsonify(user_data), 200
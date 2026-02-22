from app.model import db
from flask import request, jsonify, Blueprint
from app.model import User
from sqlalchemy.exc import IntegrityError 


user_bp = Blueprint('user', __name__)

@user_bp.route("/" , methods = ["POST"])
def add_user():
    if request.method == "POST":
        data = request.get_json()
        password_from_data = data.get("password")
        if type(password_from_data) != str:
            return jsonify({"message": "Password must be string"}), 400
        if len(password_from_data) < 6:
            return jsonify({"message": "Password must be at least 6 characters long"}), 400
        try:
            new_user = User(
                username = data.get("username"),
                email = data.get("email"),
                age = data.get("age")
            )
            new_user.set_password(password_from_data)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            error_msg = str(e.orig)
            if "uq_user_email" in error_msg:
                return jsonify({"message": "This email is already registered"}) , 400
            if "ck_user_age" in error_msg:
                return jsonify({"message":"Age must be between 5 and 100"}) , 400
            if "ck_user_username_not_empty" in error_msg:
                return jsonify({"message":"Username cannot be empty"}) , 400
            if "ck_user_email_format" in error_msg:
                return jsonify({"message":"Invalid email"}), 400
        except ValueError as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"message":"An unexpected error occurred"}) , 500
        return jsonify({"message": "User added successfully"}), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if request.method == "DELETE":
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        data = request.get_json()
        email_val = data.get("email")
        password_val = data.get("password")
    try:
        if type(password_val) != str:
            return jsonify({"message":"Password must be srting"}) , 400
        if user and user.check_password(password_val) and user.email == email_val:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"}), 200
        return jsonify({"message": "Invalid email or password"}), 401
    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig)
        if "ck_user_email_format" in error_msg:
            return jsonify({"message":"Invalid email"}), 400
    except ValueError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    except Exception as e:
            db.session.rollback()
            return jsonify({"message":"An unexpected error occurred"}) , 500

@user_bp.route('/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    data = request.get_json()
    try:
        if "username" in data:
            user.username = data.get("username")
        if "email" in data:
            user.email = data.get("email")
        if "age" in data:
            user.age = data.get("age")
        if "password" in data:
            if type(data.get("password")) != str:
                return jsonify({"message":"Password must be srting"}) , 400
            if len(data.get("password")) < 6:
                return jsonify({"message":"Password must be at least 6 characters long"}), 400
            else:
                user.set_password(data.get("password"))  
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig)
        if "uq_user_email" in error_msg:
            return jsonify({"message": "This email is already registered"}) , 400
        if "ck_user_age" in error_msg:
            return jsonify({"message":"Age must be between 5 and 100"}) , 400
        if "ck_user_username_not_empty" in error_msg:
            return jsonify({"message":"Username cannot be empty"}) , 400
        if "ck_user_email_format" in error_msg:
            return jsonify({"message":"Invalid email"}), 400
    except ValueError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    except Exception as e:
            db.session.rollback()
            return jsonify({"message":"An unexpected error occurred"}) , 500
    return jsonify({"message": "User updated successfully"}), 200

@user_bp.route('/<int:user_id>' , methods=['GET'])
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

@user_bp.route('/<int:user_id>', methods=['PUT'])
def change_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    try:
        required_fields = ["username", "email", "age", "password"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": "Missing data",
                "message": f"Fields required: {', '.join(missing_fields)}"}), 400
        if type(data.get("password")) != str:
                return jsonify({"message":"Password must be srting"}) , 400
        if len(data.get("password")) < 6:
            return jsonify({"message": "Password must be at least 6 characters long"}), 400
        user.set_password(data.get("password"))
        user.username = data.get("username")
        user.email = data.get("email")
        user.age = data.get("age")
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig)
        if "uq_user_email" in error_msg:
            return jsonify({"message": "This email is already registered"}) , 400
        if "ck_user_age" in error_msg:
            return jsonify({"message":"Age must be between 5 and 100"}) , 400
        if "ck_user_username_not_empty" in error_msg:
            return jsonify({"message":"Username cannot be empty"}) , 400
        if "ck_user_email_format" in error_msg:
            return jsonify({"message":"Invalid email"}), 400
    except ValueError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400
    except Exception as e:
            db.session.rollback()
            return jsonify({"message":"An unexpected error occurred"}) , 500
    return jsonify({"message": "User information changed successfully"}), 200
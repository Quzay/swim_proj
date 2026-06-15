from app.model import db
from flask import request, jsonify, Blueprint, url_for
from flask_jwt_extended import create_access_token, create_refresh_token , jwt_required , get_jwt , get_jwt_identity
from app.model import User, UserRole, TokenBlockList, Rating, Activity, Goal, Status, user_competition_association_table, Competition
from sqlalchemy.exc import IntegrityError 
from sqlalchemy import select, func
from decimal import Decimal, ROUND_HALF_UP

user_bp = Blueprint('user', __name__)

@user_bp.post("/register")
def create_user():
    data = request.get_json()
    password_from_data = data.get("password")
    try:
        new_user = User(
            username = data.get("username"),
            email = data.get("email"),
            age = data.get("age")
        )
        if type(password_from_data) != str:
            new_user.errors.append({"message": "Password must be string"}), 422
        if len(password_from_data) < 6:
            new_user.errors.append({"message": "Password must be at least 6 characters long"}), 422 
        role_str = data.get("role" , "USER")
        role_enum = UserRole[role_str.upper()]
        
        if new_user.errors:
            return jsonify(new_user.errors) , 422
        new_user.set_password(password_from_data)
        new_user.role = role_enum
        db.session.add(new_user)
        db.session.flush()
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig)
        if "uq_user_email" in error_msg:
            new_user.errors.append({"message": "This email is already registered"}) , 422
        if "ck_user_username_not_empty" in error_msg:
            new_user.errors.append({"message":"Username cannot be empty"}) , 422
        if "ck_user_email_format" in error_msg:
            new_user.errors.append({"message":"Invalid email"}), 422
        if "ck_user_age" in error_msg:
            new_user.errors.append({"message":"Age must be between 5 and 100"}) , 422
        
    except ValueError as e:
        db.session.rollback()
        new_user.errors.append({"message": str(e)}), 422
    except Exception as e:
        db.session.rollback()
        new_user.errors.append([{"message": f"Server error: {str(e)}"}]), 500
    if new_user.errors:
        res = new_user.errors
        new_user.errors = []
        return jsonify(res) , 422
    res = []
    return jsonify({"message": "User added successfully"}), 201
    
    
@user_bp.post("/login")
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email = data.get("email")).first()
    if user and (user.check_password(data.get("password"))):
        access_token = create_access_token(identity=user.email, additional_claims={"role": user.role})
        refresh_token = create_refresh_token(identity=user.email , additional_claims={"role" : user.role})
        return jsonify(
            {
                "message":"Logged In",
                "tokens" : {
                    "access" : access_token,
                    "refresh" : refresh_token
                } 
            }
        ), 200
    return jsonify({"message":"Invalid email or password"}) , 400

@user_bp.get("/profile")
@jwt_required()
def show_profile():
    user = User.find_by_email(get_jwt_identity())
    rating = db.session.execute(select(func.sum(Rating.value)).where(Rating.user_id == user.id)).scalar_one_or_none()
    return jsonify({"message":"message", "user_details":{
        "username" : user.username,
        "email" :user.email,
        "age" : user.age,
        "created_at" : user.created_at,
        "user_id" : user.id,
        "rating": rating or 0
        }})

@user_bp.get("/refresh")
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    user = User.find_by_email(identity)
    new_access_token = create_access_token(identity=identity, additional_claims={"role" : user.role})
    return jsonify({"access_token": new_access_token})

@user_bp.get("/logout")
@jwt_required(verify_type=False)
def logout_user():
    jwt = get_jwt()
    jti = jwt.get("jti")
    token_type =jwt.get("type")
    token_b = TokenBlockList(jti=jti)
    token_b.save()
    return jsonify ({"message":f"{token_type} token revoked successful"}), 200

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
                "message": f"Fields required: {', '.join(missing_fields)}"}), 422
        if type(data.get("password")) != str:
                return jsonify({"message":"Password must be srting"}) , 422
        if len(data.get("password")) < 6:
            return jsonify({"message": "Password must be at least 6 characters long"}), 422
        user.set_password(data.get("password"))
        user.username = data.get("username")
        user.email = data.get("email")
        user.age = data.get("age")
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig)
        if "uq_user_email" in error_msg:
            return jsonify({"message": "This email is already registered"}) , 422
        if "ck_user_age" in error_msg:
            return jsonify({"message":"Age must be between 5 and 100"}) , 422
        if "ck_user_username_not_empty" in error_msg:
            return jsonify({"message":"Username cannot be empty"}) , 422
        if "ck_user_email_format" in error_msg:
            return jsonify({"message":"Invalid email"}), 422
    except ValueError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 422
    except Exception as e:
            db.session.rollback()
            return jsonify({"message":"An unexpected error occurred"}) , 500
    return jsonify({"message": "User information changed successfully"}), 200


@user_bp.get("/<int:user_id>/")
@jwt_required()
def all_info_user(user_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"message":"You dont have permission"}) , 403
    user = db.session.get(User,user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    completed_goal = db.session.execute(select(func.count(Goal.id)).where(Goal.status == Status.COMPLETED , Goal.user_id == user_id)).scalar_one_or_none()
    activities = db.session.scalar(select(func.count(Activity.id)).where(Activity.user_id == user_id))
    rating = db.session.execute(select(func.sum(Rating.value)).where(Rating.user_id == user_id)).scalar_one_or_none()
    competition = db.session.scalar(select(func.count(user_competition_association_table.c.user_id)).where(user_competition_association_table.c.user_id == user_id))
    active_cometition = db.session.scalar(select(func.count(Competition.id))
                                          .join(user_competition_association_table,user_competition_association_table.c.user_id == user_id)
                                          .where(Competition.id == user_competition_association_table.c.competition_id , Competition.status == Status.ACTIVE)
                                          )
    rating_rounded = Decimal(str(rating)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    distance_rounded = Decimal(str(user.total_distance/1000)).quantize(Decimal("0.01") , rounding=ROUND_HALF_UP)
    user_data = {               
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "created_at": user.created_at.isoformat(),
        "activity_cont" : user.activity_count,
        "completed_goal_count" : completed_goal if completed_goal else 0,
        "total_rating" : rating_rounded if rating_rounded else 0 ,
        "competition_joined" : competition if competition else 0 ,
        "joined_active_competition" : active_cometition if active_cometition else 0 ,
        "total_distance" : f"{distance_rounded} km" if distance_rounded else 0,
        "Links" : {
            "list_activity" : url_for("activity.show_all_activities", user_id = user_id),
            "list_goal" : url_for("goal.show_all_goals" , user_id = user_id),
            "link_competition" : url_for("competition.show_take_part" , user_id =user_id) #!!!!!!!!!!!!!!! Закінчити
        }
    }
    return jsonify(user_data) , 200

def create_user_logic(data):
    password_from_data = data.get("password")
    try:
        new_user = User(
            username = data.get("username"),
            email = data.get("email"),
            age = data.get("age"),
            facebook_id = data.get("facebook_id")
        )
        if type(password_from_data) != str:
            new_user.errors.append({"message": "Password must be string"}), 422
        if len(password_from_data) < 6:
            new_user.errors.append({"message": "Password must be at least 6 characters long"}), 422 
        role_str = data.get("role" , "USER")
        role_enum = UserRole[role_str.upper()]
        
        if new_user.errors:
            return jsonify(new_user.errors) , 422
        new_user.set_password(password_from_data)
        new_user.role = role_enum
        db.session.add(new_user)
        db.session.flush()
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig)
        if "uq_user_email" in error_msg:
            new_user.errors.append({"message": "This email is already registered"}) , 422
        if "ck_user_username_not_empty" in error_msg:
            new_user.errors.append({"message":"Username cannot be empty"}) , 422
        if "ck_user_email_format" in error_msg:
            new_user.errors.append({"message":"Invalid email"}), 422
        if "ck_user_age" in error_msg:
            new_user.errors.append({"message":"Age must be between 5 and 100"}) , 422
        
    except ValueError as e:
        db.session.rollback()
        new_user.errors.append({"message": str(e)}), 422
    except Exception as e:
        db.session.rollback()
        new_user.errors.append([{"message": f"Server error: {str(e)}"}]), 500
    if new_user.errors:
        res = new_user.errors
        new_user.errors = []
        return jsonify(res) , 422
    res = []
    return new_user, None
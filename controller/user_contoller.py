from model import db,app
from flask import request, jsonify
from model.user import User



@app.route("/user/add" , methods = ["POST"])
def add_user():
    if request.method == "POST":
        data = request.get_json()
        name_from_data = data.get("username")
        email_from_data = data.get("email")
        age_from_data = data.get("age")
        password_from_data = data.get("password")
        
        user = User(username = name_from_data,email = email_from_data, age = age_from_data,password = password_from_data)
        db.session.add(user)
        db.session.commit()
        return jsonify ({"message" : "User created successful" }), 201

        
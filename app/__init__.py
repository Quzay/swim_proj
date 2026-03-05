import os
from flask import Flask , jsonify
from .model.base import db,jwt
from .model import User , TokenBlockList
from dotenv import load_dotenv


load_dotenv()

def create_app(config = None):
    app = Flask(__name__)
    app.config.from_prefixed_env()

    if not config:
        url = (os.environ.get("LINK_DB"))
        app.config["SQLALCHEMY_DATABASE_URI"] = url
    else:
        app.config.from_mapping(config)

    db.init_app(app)
    jwt.init_app(app)
    from .controller.users import users_bp
    from .controller.user_contoller import user_bp
    from .controller.activity_controller import activity_bp
    from .controller.goal_controller import goal_bp
    from .controller.competition_controller import competition_bp
    
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(activity_bp, url_prefix="/activity")
    app.register_blueprint(goal_bp, url_prefix = "/goal")
    app.register_blueprint(competition_bp, url_prefix = "/competition")
    app.register_blueprint(users_bp, url_prefix ='/users')


    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers,jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(email = identity).one_or_none()

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_data):
        return jsonify({"message":"Token has expired", "error":"token_expired"}) , 401  

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message":"Signature verification failed", "error":"invalid_token"}) , 401  

    @jwt.unauthorized_loader 
    def missing_token_callback(error):
        return jsonify({"message":"Request does not contain a valid token", "error":"autarization_header"}) , 401  
     
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data.get('jti')
        token = db.session.query(TokenBlockList).filter(TokenBlockList.jti == jti).scalar()
        return token is not None

    with app.app_context():
        db.create_all()
    return app
        

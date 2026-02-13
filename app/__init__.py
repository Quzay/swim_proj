import os
from flask import Flask
from .model.base import db
from dotenv import load_dotenv


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    url = (os.environ.get("LINK_DB"))
    app.config["SQLALCHEMY_DATABASE_URI"] = url

    db.init_app(app)

    from .controller.user_contoller import user_bp
    from .controller.activity_controller import activity_bp
    from .controller.goal_controller import goal_bp
    
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(activity_bp, url_prefix="/activity")
    app.register_blueprint(goal_bp, url_prefix = "/goal")

    with app.app_context():
        db.create_all()
    return app
        

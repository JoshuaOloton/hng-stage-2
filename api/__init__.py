from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .organisations import organisations as orgs_blueprint
    app.register_blueprint(orgs_blueprint, url_prefix='/api')

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/api')

    app.json.sort_keys = False

    return app

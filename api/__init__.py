from flask import Flask
from config import config

def create_app(config_name='default'):

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Add your app configuration and routes here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api')

    return app

app = create_app()
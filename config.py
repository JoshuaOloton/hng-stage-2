import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
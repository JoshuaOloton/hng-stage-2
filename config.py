from datetime import timedelta
from os import environ
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5) # jwt token expires after 5 minutes

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'hng.db')
    # SQLALCHEMY_DATABASE_URI = 'postgres://postgres:next23rd@localhost:5432/hng-stage-1'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://scott:tiger@localhost/project'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'dialect://username:password@host:port/database'

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
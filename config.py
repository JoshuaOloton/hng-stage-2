from os import environ
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5) # jwt token expires after 5 minutes

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'hng_test.db')

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:next23rd@localhost:5432/hngstage2'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'hng_dev.db')
    # SQLALCHEMY_DATABASE_URI = 'dialect://username:password@host:port/database'


class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'hng_prod.db')
    # SQLALCHEMY_DATABASE_URI = f"postgresql://josh:{environ.get('POSTGRES_PASSWORD')}@dpg-cq5am3tds78s73curaf0-a.oregon-postgres.render.com/hngstage2_b0fc"
    SQLALCHEMY_DATABASE_URI = f"postgresql://josh-hng11-main-db-0ebe030356e075745:{environ.get('POSTGRES_PASSWORD')}@user-prod-us-east-2-1.cluster-cfi5vnucvv3w.us-east-2.rds.amazonaws.com:5432/josh-hng11-main-db-0ebe030356e075745"

config = {
    'default': DevelopmentConfig,
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
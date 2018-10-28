import os
import configparser
basedir = os.path.abspath(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read('config.ini')

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = config['APP_SETTINGS']['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = config['APP_SETTINGS']['DATABASE_URI']

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

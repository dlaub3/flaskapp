#!/usr/bin/python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from healthcheck import HealthCheck, EnvironmentDump
import os
import configparser
from config import DevelopmentConfig
from pprint import pprint
from flask import Flask, jsonify

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['FLASK_DEBUG'] = 1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:root@db:5432/flaskapp'
db = SQLAlchemy(app)

health = HealthCheck(app, "/healthcheck")
envdump = EnvironmentDump(app, "/environment")

def database_status():
    working = True
    output = 'database is ok'

    try:
        session = db.session()
        session.execute('SELECT 1')
    except Exception as e:
        output = str(e)
        working = False

    return working, output

health.add_check(database_status)


@app.route("/ping", methods=['GET'])
def hello():
    return "pong"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

    
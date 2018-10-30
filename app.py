#!/usr/bin/python

from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from healthcheck import HealthCheck, EnvironmentDump
from models import *
from forms import *
import json

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:root@db:5432/flaskapp'
app.config['FLASK_DEBUG'] = 1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
def ping():
    return "pong"

@app.route("/user", methods=['POST'])
def add_user():
    form = UserForm()
    user = User()
    fields = ('first_name', 'last_name', 'date_of_birth')
    for field in fields:
        setattr(user, field, getattr(form, field).data);
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        Response(response='{"status": "server error"}', status=500, headers=None, mimetype=None, content_type='application/json', direct_passthrough=False)
    return jsonify( first_name=user.first_name, last_name=user.last_name, date_of_birth=user.date_of_birth )

@app.route("/user/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    return jsonify( first_name=user.first_name, last_name=user.last_name, date_of_birth=user.date_of_birth )

@app.route("/user/<int:user_id>", methods=['PUT'])
def update_user(user_id):
    form = UserForm()
    user = db.session.query(User).filter_by(id=user_id).first()
    fields = ('first_name', 'last_name', 'date_of_birth')
    for field in fields:
        setattr(user, field, getattr(form, field).data);
    db.session.commit()
    return jsonify( first_name=user.first_name, last_name=user.last_name, date_of_birth=user.date_of_birth )

@app.route("/user/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify(id=user_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


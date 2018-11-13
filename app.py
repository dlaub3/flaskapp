#!/usr/bin/python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from healthcheck import HealthCheck, EnvironmentDump
from flask_cors import CORS
from flask_restless import APIManager
from datetime import datetime

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:root@db:5432/flaskapp'
app.config['FLASK_DEBUG'] = 1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)

health = HealthCheck(app, "/api/healthcheck")
envdump = EnvironmentDump(app, "/api/environment")


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date())
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    addresses = db.relationship(
        'Address', cascade="all,delete", backref='Person', lazy='dynamic')
    email_addresses = db.relationship(
        'EmailAddress', cascade="all,delete", backref='Person', lazy='dynamic')
    phone_numbers = db.relationship(
        'PhoneNumber', cascade="all,delete", backref='Person', lazy='dynamic')


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey(
        "person.id"), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    address_1 = db.Column(db.String(128))
    address_2 = db.Column(db.String(128))
    city = db.Column(db.String(128))
    state = db.Column(db.String(128))
    zip = db.Column(db.Integer())
    country = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)


class EmailAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey(
        "person.id"), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    email_address = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)


class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey(
        "person.id"), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    phone_number = db.Column(db.String(128))  # db.Integer() max of 9
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)


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


@app.route("/api/ping", methods=['GET'])
def ping():
    return "pong"


manager = APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.

# include_filters = ['first_name', 'last_name', 'date_of_birth',
#                    'phone_numbers.phone_number', 'email_addresses.email_address']
# manager.create_api(
#     Person, methods=['GET', 'POST', 'PUT', 'DELETE'], exclude_columns=filters_person include_columns=[''])

manager.create_api(Person, methods=['GET', 'POST', 'PUT', 'DELETE'])

manager.create_api(Type, methods=['GET', 'POST', 'PUT', 'DELETE'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

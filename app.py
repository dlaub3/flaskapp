#!/usr/bin/python

from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import DevelopmentConfig
from healthcheck import HealthCheck, EnvironmentDump
from models import *
from forms import *
from flask_cors import CORS
import json
import decimal
import datetime

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:root@db:5432/flaskapp'
app.config['FLASK_DEBUG'] = 1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)

health = HealthCheck(app, "/healthcheck")
envdump = EnvironmentDump(app, "/environment")

filters = set(['created_at', 'updated_at'])


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


def sql_search_builder(schema, args):
    query = dict()
    sql_query = dict()
    for field in args:
        query[field] = '%' + args.get(field) + '%'
        sql_query[field] = field + '::text' + ' ilike :' + field

    where = ' AND '.join(v for v in sql_query.values())
    sql = 'SELECT * FROM ' + schema + ' where ' + where
    return sql, query


def object_to_json(obj, obj_fields):
    # http://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
    def alchemyencoder(obj):
        """JSON encoder function for SQLAlchemy special classes."""
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)

    def map_json(obj):
        json_data = dict()
        for field in obj_fields:
            json_data[field] = getattr(obj, field)
        return json_data

    objson = json.dumps([map_json(o)
                         for o in obj], default=alchemyencoder)
    return objson


# @improvement - how to generate person_fields from model?
# Person
person_fields = ('id', 'first_name', 'last_name', 'date_of_birth')


@app.route("/person", methods=['GET'])
def search_person():
    sql, query = sql_search_builder('person', request.args)
    results = db.session.query(Person).from_statement(
        text(sql)).params(**query).all()

    return object_to_json(results, person_fields)


@app.route("/person", methods=['POST'])
def add_person():
    form = PersonForm()
    person = Person()
    json_data = dict()
    for field in person_fields:
        app.logger.warning(vars(form))
        if field == 'id':
            continue
        json_data[field] = getattr(form, field).data
        setattr(person, field, getattr(form, field).data)
    try:
        saved = db.session.add(person)
        db.session.commit()
        json_data['id'] = person.id
    except Exception as e:
        Response(response='{"status": "server error"}', status=500, headers=[
                 'Access-Control-Allow-Origin', '*'], mimetype=None, content_type='application/json', direct_passthrough=False)

    return jsonify(json_data)


@app.route("/person/<int:person_id>", methods=['GET'])
def get_person(person_id):
    person = db.session.query(Person).filter_by(id=person_id).first()
    json_data = dict()
    for field in person_fields:
        json_data[field] = getattr(person, field)
    return jsonify(json_data)


@app.route("/person/<int:person_id>", methods=['PUT'])
def update_person(person_id):
    form = PersonForm()
    person = db.session.query(Person).filter_by(id=person_id).first()
    json_data = dict()
    for field in person_fields:
        json_data[field] = getattr(form, field).data
        setattr(person, field, getattr(form, field).data)
    db.session.commit()
    return jsonify(json_data)


@app.route("/person/<int:person_id>", methods=['DELETE'])
def delete_person(person_id):
    person = db.session.query(Person).filter_by(id=person_id).first()
    json_data = dict()
    for field in person_fields:
        json_data[field] = getattr(person, field)
    db.session.delete(person)
    db.session.commit()
    return jsonify(json_data)


# Address
address_fields = ('person_id', 'type_id', 'address_1',
                  'address_2', 'city', 'state', 'zip', 'country')


@app.route("/address", methods=['GET'])
def search_address():
    sql, query = sql_search_builder('address', request.args)
    results = db.session.query(Address).from_statement(
        text(sql)).params(**query).all()

    return object_to_json(results, address_fields)


@app.route("/address", methods=['POST'])
def add_address():
    form = AddressForm()
    address = Address()
    json_data = dict()
    for field in address_fields:
        json_data[field] = getattr(form, field).data
        setattr(address, field, getattr(form, field).data)
    try:
        db.session.add(address)
        db.session.commit()
    except Exception as e:
        Response(response='{"status": "server error"}', status=500, headers=None,
                 mimetype=None, content_type='application/json', direct_passthrough=False)

    return jsonify(json_data)


@app.route("/address/<int:address_id>", methods=['GET'])
def get_address(address_id):
    address = db.session.query(Address).filter_by(id=address_id).first()
    json_data = dict()
    for field in address_fields:
        json_data[field] = getattr(address, field)
    return jsonify(json_data)


@app.route("/address/<int:address_id>", methods=['PUT'])
def update_address(address_id):
    form = AddressForm()
    address = db.session.query(Address).filter_by(id=address_id).first()
    json_data = dict()
    for field in address_fields:
        setattr(address, field, getattr(form, field).data)
        json_data[field] = getattr(form, field).data
    db.session.commit()
    return jsonify(json_data)


@app.route("/address/<int:address_id>", methods=['DELETE'])
def delete_address(address_id):
    address = db.session.query(Address).filter_by(id=address_id).first()
    json_data = dict()
    for field in address_fields:
        json_data[field] = getattr(address, field)
    db.session.delete(address)
    db.session.commit()
    return jsonify(json_data)


# Email
email_address_fields = ('person_id', 'type_id', 'email_address')


@app.route("/email-address", methods=['GET'])
def search_email_address():
    sql, query = sql_search_builder('email_address', request.args)
    results = db.session.query(EmailAddress).from_statement(
        text(sql)).params(**query).all()

    return object_to_json(results, email_address_fields)


@app.route("/email-address", methods=['POST'])
def add_email_address():
    form = EmailAddressForm()
    email_address = EmailAddress()
    json_data = dict()
    for field in email_address_fields:
        json_data[field] = getattr(form, field).data
        setattr(email_address, field, getattr(form, field).data)
    try:
        db.session.add(email_address)
        db.session.commit()
    except Exception as e:
        Response(response='{"status": "server error"}', status=500, headers=None,
                 mimetype=None, content_type='application/json', direct_passthrough=False)

    return jsonify(json_data)


@app.route("/email-address/<int:email_address_id>", methods=['GET'])
def get_email_address(email_address_id):
    email_address = db.session.query(
        EmailAddress).filter_by(id=email_address_id).first()
    json_data = dict()
    for field in email_address_fields:
        json_data[field] = getattr(email_address, field)
    return jsonify(json_data)


@app.route("/email-address/<int:email_address_id>", methods=['PUT'])
def update_email_address(email_address_id):
    form = EmailAddressForm()
    email_address = db.session.query(
        EmailAddress).filter_by(id=email_address_id).first()
    json_data = dict()
    for field in email_address_fields:
        setattr(email_address, field, getattr(form, field).data)
        json_data[field] = getattr(form, field).data
    db.session.commit()
    return jsonify(json_data)


@app.route("/email-address/<int:email_address_id>", methods=['DELETE'])
def delete_email_address(email_address_id):
    email_address = db.session.query(
        EmailAddress).filter_by(id=email_address_id).first()
    json_data = dict()
    for field in email_address_fields:
        json_data[field] = getattr(email_address, field)
    db.session.delete(email_address)
    db.session.commit()
    return jsonify(json_data)


# PhoneNumber
phone_number_fields = ('person_id', 'type_id', 'phone_number')


@app.route("/phone-number", methods=['GET'])
def search_phone_number():
    sql, query = sql_search_builder('phone_number', request.args)
    results = db.session.query(PhoneNumber).from_statement(
        text(sql)).params(**query).all()

    return object_to_json(results, phone_number_fields)


@app.route("/phone-number", methods=['POST'])
def add_phone_number():
    form = PhoneNumberForm()
    phone_number = PhoneNumber()
    json_data = dict()
    for field in phone_number_fields:
        json_data[field] = getattr(form, field).data
        setattr(phone_number, field, getattr(form, field).data)
    try:
        db.session.add(phone_number)
        db.session.commit()
    except Exception as e:
        Response(response='{"status": "server error"}', status=500, headers=None,
                 mimetype=None, content_type='application/json', direct_passthrough=False)

    return jsonify(json_data)


@app.route("/phone-number/<int:phone_number_id>", methods=['GET'])
def get_phone_number(phone_number_id):
    phone_number = db.session.query(
        PhoneNumber).filter_by(id=phone_number_id).first()
    json_data = dict()
    for field in phone_number_fields:
        json_data[field] = getattr(phone_number, field)
    return jsonify(json_data)


@app.route("/phone-number/<int:phone_number_id>", methods=['PUT'])
def update_phone_number(phone_number_id):
    form = PhoneNumberForm()
    phone_number = db.session.query(
        PhoneNumber).filter_by(id=phone_number_id).first()
    json_data = dict()
    for field in phone_number_fields:
        setattr(phone_number, field, getattr(form, field).data)
        json_data[field] = getattr(form, field).data
    db.session.commit()
    return jsonify(json_data)


@app.route("/phone-number/<int:phone_number_id>", methods=['DELETE'])
def delete_phone_number(phone_number_id):
    phone_number = db.session.query(
        PhoneNumber).filter_by(id=phone_number_id).first()
    json_data = dict()
    for field in phone_number_fields:
        json_data[field] = getattr(phone_number, field)
    db.session.delete(phone_number)
    db.session.commit()
    return jsonify(json_data)


# Type
type_fields = ('type',)


@app.route("/type", methods=['POST'])
def add_type():
    form = TypeForm()
    type = Type()
    json_data = dict()
    for field in type_fields:
        json_data[field] = getattr(form, field).data
        setattr(type, field, getattr(form, field).data)
    try:
        db.session.add(type)
        db.session.commit()
    except Exception as e:
        Response(response='{"status": "server error"}', status=500, headers=None,
                 mimetype=None, content_type='application/json', direct_passthrough=False)

    return jsonify(json_data)


@app.route("/type/<int:type_id>", methods=['GET'])
def get_type(type_id):
    type = db.session.query(Type).filter_by(id=type_id).first()
    json_data = dict()
    for field in type_fields:
        json_data[field] = getattr(type, field)
    return jsonify(json_data)


@app.route("/type/<int:type_id>", methods=['PUT'])
def update_type(type_id):
    form = TypeForm()
    type = db.session.query(Type).filter_by(id=type_id).first()
    json_data = dict()
    for field in type_fields:
        setattr(type, field, getattr(form, field).data)
        json_data[field] = getattr(form, field).data
    db.session.commit()
    return jsonify(json_data)


@app.route("/type/<int:type_id>", methods=['DELETE'])
def delete_type(type_id):
    type = db.session.query(Type).filter_by(id=type_id).first()
    json_data = dict()
    for field in type_fields:
        json_data[field] = getattr(type, field)
    db.session.delete(type)
    db.session.commit()
    return jsonify(json_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

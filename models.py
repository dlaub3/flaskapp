from app import db
from datetime import datetime

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date())
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    addresses = db.relationship('Address', backref='Person', lazy=True)
    email_address = db.relationship('EmailAddress', backref='Person', lazy=True)
    phone_number = db.relationship('PhoneNumber', backref='Person', lazy=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
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
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    email_address = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    phone_number = db.Column(db.Integer())
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
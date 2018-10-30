from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date())
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    address_1 = db.Column(db.String(128))
    address_2 = db.Column(db.String(128))
    city = db.Column(db.String(128))
    state = db.Column(db.String(128))
    zip = db.Column(db.Integer())
    country = db.Column(db.String(128))
    type = db.Column(db.Integer())
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    email_address = db.Column(db.String(128))
    type = db.Column(db.Integer())
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

class PhoneNumbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    phone_number = db.Column(db.Integer())
    type = db.Column(db.Integer())
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
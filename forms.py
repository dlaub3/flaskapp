from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class PersonForm(FlaskForm):
    id = StringField('id')
    first_name = StringField('first_name')
    last_name = StringField('last_name')
    date_of_birth = StringField('date_of_birth')

class EmailAddressForm(FlaskForm):
    id = StringField('id')
    type_id = StringField('type_id', validators=[DataRequired()])
    person_id = StringField('person_id', validators=[DataRequired()])
    email_address = StringField('email_address', validators=[DataRequired()])

class PhoneNumberForm(FlaskForm):
    id = StringField('id')
    person_id = StringField('person_id', validators=[DataRequired()])
    type_id = StringField('type_id', validators=[DataRequired()])
    phone_number = StringField('phone_number', validators=[DataRequired()])

class AddressForm(FlaskForm):
    id = StringField('id')
    person_id = StringField('person_id', validators=[DataRequired()])
    type_id = StringField('type_id', validators=[DataRequired()])
    address_1 = StringField('address_1', validators=[DataRequired()])
    address_2 = StringField('address_2')
    city = StringField('city', validators=[DataRequired()])
    state = StringField('state', validators=[DataRequired()])
    zip = StringField('zip', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])

class TypeForm(FlaskForm):
    id = StringField('id')
    type = StringField('type', validators=[DataRequired()])
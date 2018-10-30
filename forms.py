from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    first_name = StringField('first_name')
    last_name = StringField('last_name')
    date_of_birth = StringField('date_of_birth')

class EmailForm(FlaskForm):
    email_address = StringField('email_address', validators=[DataRequired()])
    type = StringField('type', validators=[DataRequired()])

class PhoneForm(FlaskForm):
    phone_number = StringField('email_address', validators=[DataRequired()])
    type = StringField('type', validators=[DataRequired()])

class AddressForm(FlaskForm):
    address_1 = StringField('address_1', validators=[DataRequired()])
    address_2 = StringField('address_2')
    city = StringField('city', validators=[DataRequired()])
    state = StringField('state', validators=[DataRequired()])
    zip = StringField('zip', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])
    type = StringField('type', validators=[DataRequired()])
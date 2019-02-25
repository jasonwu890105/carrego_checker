from app import db
from flask_wtf import Form, FlaskForm
from wtforms import Form, StringField, SelectField, RadioField, DateField, IntegerField, ValidationError, validators, PasswordField, BooleanField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, DataRequired
from .util.validator import Unique
from app.models import Cars

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CarSearchForm(Form):

    choices = [('State', "State"),
               ('Rego', 'Rego'),
               ('Driver', 'Driver')]
    
    select = SelectField('Search for cars:', choices=choices)
    search = StringField('')



class CarsForm(Form):
    state_select = [('NSW', "NSW"),
               ('ACT', 'ACT'),
               ('QLD', 'QLD'),
               ('SA', 'SA'),
               ('WA', 'WA'),
               ('NT', 'NT'),
               ('VIC', 'VIC')]

    regonum = StringField('Rego', validators=[InputRequired(message='Please Enter a valid rego number'),Unique(Cars, Cars.regonum, message='This Car Has Already Registered')])
    make = StringField('Make')
    model = StringField('Model')
    engine_size = StringField('Engine Size')
    year_manufactured = StringField('Year Manuafactured')
    value_insured = StringField('Insured Value')
    owenership = StringField('Owndership')
    motorcharge_card = StringField('MotorCharge Card #')
    house_location = StringField('Housed Location')
    driver = StringField('Driver', validators=[InputRequired(message="Please Enter a Driver.")])
    state = SelectField('State', choices=state_select, validators=[InputRequired()])
    manager = StringField('Manager', validators=[InputRequired(message="Please Enter Manager's Name.")])
    expirydate = DateField('ExpiryDate', format='%d/%m/%Y')
    email = StringField('Email', validators=[InputRequired(message="Please Enter a Email Address.")])
    

class CarsForm_Update(Form):
    state_select = [('NSW', "NSW"),
               ('ACT', 'ACT'),
               ('QLD', 'QLD'),
               ('SA', 'SA'),
               ('WA', 'WA'),
               ('NT', 'NT'),
               ('VIC', 'VIC')]

    regonum = StringField('Rego')
    make = StringField('Make')
    model = StringField('Model')
    engine_size = StringField('Engine Size')
    year_manufactured = StringField('Year Manuafactured')
    value_insured = StringField('Insured Value')
    owenership = StringField('Owndership')
    motorcharge_card = StringField('MotorCharge Card #')
    house_location = StringField('Housed Location')
    driver = StringField('Driver', validators=[InputRequired(message="Please Enter a Driver.")])
    state = SelectField('State', choices=state_select)
    manager = StringField('Manager', validators=[InputRequired(message="Please Enter Manager's Name.")])
    expirydate = DateField('ExpiryDate', format='%d/%m/%Y')
    email = StringField('Email', validators=[InputRequired(message="Please Enter a Email Address.")])



def choice_query():

        return db.session.query(Cars.manager.distinct())
        
def get_pk(obj):
    return str(obj)

class DownloadForm(FlaskForm):

    category = QuerySelectField(query_factory=choice_query, allow_blank=True, get_pk=get_pk)
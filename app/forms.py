from app import db
from flask_wtf import Form, FlaskForm
from wtforms import Form, StringField, SelectField, RadioField, DateField, IntegerField, ValidationError, validators
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired
from .util.validator import Unique
from app.models import Cars


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

    regonum = StringField('Rego', validators=[Unique(Cars, Cars.regonum, message='This Car Has Already Registered')])
    driver = StringField('Driver', validators=[InputRequired(message="Please Enter a Driver.")])
    state = SelectField('State', choices=state_select)
    manager = StringField('Manager', validators=[InputRequired(message="Please Enter Manager's Name.")])
    expirydate = DateField('ExpiryDate', format='%d/%m/%Y')
    email = StringField('Email', validators=[InputRequired(message="Please Enter a Email Address.")])
    #rego_daysleft = IntegerField('Exprting In')

class CarsForm_Update(Form):
    state_select = [('NSW', "NSW"),
               ('ACT', 'ACT'),
               ('QLD', 'QLD'),
               ('SA', 'SA'),
               ('WA', 'WA'),
               ('NT', 'NT'),
               ('VIC', 'VIC')]

    regonum = StringField('Rego')
    driver = StringField('Driver', validators=[InputRequired(message="Please Enter a Driver.")])
    state = SelectField('State', choices=state_select)
    manager = StringField('Manager', validators=[InputRequired(message="Please Enter Manager's Name.")])
    expirydate = DateField('ExpiryDate', format='%d/%m/%Y')
    email = StringField('Email', validators=[InputRequired(message="Please Enter a Email Address.")])


'''
def choice_query():
    return db.session.query(Cars.manager).all()
'''

def choice_query():

        return db.session.query(Cars.manager.distinct())
        
def get_pk(obj):
    return str(obj)

class DownloadForm(FlaskForm):

    category = QuerySelectField(query_factory=choice_query, allow_blank=True, get_pk=get_pk)
from app import login
from app import db
import datetime
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property
from sqlalchemy import extract
from sqlalchemy.orm import validates
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regonum = db.Column(db.String(15), index=True, unique=True, nullable=False)
    driver = db.Column(db.String(50), index=True)
    state = db.Column(db.String(20), index=True, nullable=False)
    manager = db.Column(db.String(50), nullable=False)
    expirydate = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(), nullable=False)
    #rego_daysleft = column_property((datetime.strftime(expirydate, '%d/%m/%Y') - date.today().strftime('%d/%m/%Y')).days)
    #rego_daysleft = db.Column(db.Integer)

    @hybrid_property
    def rego_daysleft(self):
        #self.expirydate = datetime.strptime(self.expirydate, '%d/%m/%Y')
        self.today = datetime.now()
        return (self.expirydate - self.today).days

    @rego_daysleft.expression
    def rego_daysleft(cls):
        cls.today = datetime.now()
        cls.daysleft = cls.expirydate - cls.today
        return extract('day', cls.daysleft)

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<User {}>'.format(self.username)   


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
from app import db
import datetime
from datetime import datetime, date
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property
from sqlalchemy import extract
from sqlalchemy.orm import validates


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

'''
    @validates('regonum')
    def validate_regonum(self, key, regonum):
        if Cars.query.filter(Cars.regonum == regonum).first():
            raise AssertionError('Rego Plate Numer has already been registered!!!')
        
        return regonum
'''

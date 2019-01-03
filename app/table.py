from flask_table import Table, Col, LinkCol, ButtonCol
 
class Results(Table):
    id = Col('Id', show=False)
    regonum = Col('Regonum')
    driver = Col('Driver')
    state = Col('State')
    manager = Col('Manager')
    expirydate = Col('Expirydate')
    email = Col('Email')
    rego_daysleft = Col('Exprting In')
    edit = ButtonCol('Edit', 'edit', url_kwargs=dict(id='id'))
    delete = ButtonCol('Delete', 'delete', url_kwargs=dict(id='id'))
    renew = ButtonCol('Renew_One_Year', 'renew', url_kwargs=dict(id='id'))
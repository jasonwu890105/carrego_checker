from flask_table import Table, Col, LinkCol
 
class Results(Table):
    id = Col('Id', show=False)
    regonum = Col('Regonum')
    driver = Col('Driver')
    state = Col('State')
    manager = Col('Manager')
    expirydate = Col('Expirydate')
    email = Col('Email')
    rego_daysleft = Col('Exprting In')
    #rego_daysleft = Col('Rego Remaining')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))
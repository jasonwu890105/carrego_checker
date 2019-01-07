from app import app, db
from flask import render_template, request, redirect, flash, jsonify, session, url_for, send_file
from app.forms import CarSearchForm, CarsForm, DownloadForm, CarsForm_Update
from app.models import Cars
from app.table import Results
import csv
import flask_excel as excel
import pandas as pd 
import json, datetime
from pandas.io.json import json_normalize
from io import TextIOWrapper 
from sqlalchemy import create_engine
import datetime, datedelta

@app.route('/', methods=['GET', 'POST'])
#@app.route('/index', methods=['GET', 'POST'])
def index():
    search = CarSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.htm', form=search)

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Rego':
            qry = Cars.query.filter(Cars.regonum.ilike(search_string))
            results = qry.all()
        elif search.data['select'] == 'State':
            qry = Cars.query.filter(Cars.state.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'Driver':
            qry = Cars.query.filter(Cars.driver.ilike(search_string))
            results = qry.all()
    
    else:
        qry = Cars.query
        results = qry.all()

    if not results:
        flash ('No results found!')
        return redirect('/')
    
    else:
        table = Results(results)
        table.border = True
        return render_template('results.htm', table=table)

'''
        def export_csv():
            #csvfile = cStringIO.StringIO()
            csvfile = StringIO.StringIO()
            headers = [
                'RegoPlate',
                'Driver',
                'State',
                'Manager',
                'ExpiryDate',
                'Email'
            ]

            rows = []
            for result in results:
                rows.append(
                    {
                        'RegoPlate' : result.regonum,
                        'Driver': result.driver,
                        'State' : result.state,
                        'Manager': result.manager,
                        'ExpiryDate': result.expirydate,
                        'Email' : result.email
                    }
                )

'''


@app.route('/new_cars', methods=['GET', 'POST'])
def new_cars():
    form = CarsForm(request.form)

    if request.method == 'POST' and form.validate():
        car = Cars()
    
        save_changes(car, form, new=True)
        flash('New Car has been successfully registered!')
        return redirect('/')

            #return jsonify(msg='Car successfully registered', car_plate=car.regonum), 200
        '''
        except AssertionError as exception_message:
            
            return jsonify(msg='Error: {}. '.format(exception_message)), 400
        '''

    else:
        return render_template('new_cars.htm', form=form, message='Rego already exit')

    if request.method == 'GET':
        return render_template('new_cars.htm', form=form)

def save_changes(car, form, new=False):

    car.regonum = form.regonum.data.lower()
    car.driver = form.driver.data.lower()
    car.state = form.state.data.lower()
    car.manager = form.manager.data.lower()
    car.expirydate = form.expirydate.data
    car.email = form.email.data.lower()

    if new:
        # Add the new car to the database
        db.session.add(car)
 
    # commit the data to the database
    db.session.commit()

def update_changes(car, form):

    car.regonum = form.regonum.data.lower()
    car.driver = form.driver.data.lower()
    car.state = form.state.data.lower()
    car.manager = form.manager.data.lower()
    car.expirydate = form.expirydate.data
    car.email = form.email.data.lower()
    db.session.commit()

@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = Cars.query.filter(Cars.id==id)
    car = qry.first()

    if car:
        form = CarsForm_Update(formdata=request.form, obj=car)
        if request.method == 'POST' and form.validate():

            # save edits

            update_changes(car, form)
            flash('Rego updated successfully!')
            return redirect('/')
        return render_template('edit_car.htm', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    qry = Cars.query.filter(Cars.id==id)
    car = qry.first()

    if car:
        form = CarsForm_Update(formdata=request.form, obj=car)
        if request.method == 'POST' and form.validate():
            db.session.delete(car)
            db.session.commit()

            flash('Car deleted successfully!')
            return redirect('/')
        
        return render_template('delete_car.htm', form=form)

    else:
        return 'Error deleting #{id}'.format(id=id)
    
@app.route('/renew/<int:id>', methods=['GET', 'POST'])
def renew(id):
    qry = Cars.query.filter(Cars.id==id)
    car = qry.first()

    #if car:
    #    form = CarsForm_Update(formdata=request.form, obj=car)
    if request.method == 'POST':
        car.expirydate = car.expirydate + datedelta.YEAR
        db.session.commit()

        car_rego = car.regonum
        flash(f'{car_rego} Renew for One More Year!')
        return redirect('/')
        
        #return render_template('renew_car.htm', form=form)

    else:
        return 'Error deleting #{id}'.format(id=id)
 

@app.route('/download', methods=['GET', 'POST'])
def download():

    category = DownloadForm(request.form)
    if request.method == 'POST':
        return download_results(category)

    return render_template('download.htm', form=category)

    #query_sets = []
    #download_form = DownloadForm(request.form)
    #selectedmanager = download_form.data['category']

    #if selectedmanager:
    #if download_form.validate():             #validate_on_submit():
        #selectedmanager = download_form.data['category']
    #query_sets = Cars.query.filter(Cars.manager==selectedmanager).all()
    #print(download_form.data)
        #column_name = ['id', 'regonum', 'driver', 'state', 'manager', 'expirydate']
        #return excel.make_response_from_query_sets(query_sets, column_name, 'csv')


    #return render_template('download.htm', form=download_form)
@app.route('/download_results')
def download_results(category):

    query_sets = []
    category_string = category.data['category']

    if category_string:
        query_sets = Cars.query.filter(Cars.manager==category_string).all()
        column_name = ['regonum', 'driver', 'state', 'manager', 'expirydate', 'email']
        return excel.make_response_from_query_sets(query_sets, column_name, 'csv')

    return render_template('download.htm', form=category)    

@app.route('/downloads')
def downloadsearch():
    #searchform = DownloadForm()
    #selectedmanager = searchform.category.data
    query_sets_all = Cars.query.all()
    column_name = ['regonum', 'driver', 'state', 'manager', 'expirydate', 'email']
    return excel.make_response_from_query_sets(query_sets_all, column_name, 'csv')


@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    global filename
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No selected file')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return render_template('upload.htm')

        try:
            df = pd.read_csv(file)
            filename = datetime.datetime.now().strftime("/home/jason/Desktop/carrego/app/uploads/%Y-%m-%d-%H-%M-%S-%f"+".csv")
            df.to_csv(filename, index=None)
            flash('File Uploaded Successfully')
            return render_template('upload.htm', data=df.to_html(), btn='validatecsv.htm')

        except Exception as e:
            return render_template("upload.htm", text=str(e))
    
    return render_template('upload.htm', methods=['GET', 'POST'])

@app.route("/download_file/")
def download_csv():
    return send_file(filename, attachment_filename='yourfile.csv', as_attachment=True)

'''
@app.route('/Save_to_DB', methods=['GET', 'POST'])
def save_to_db():
    engine = create_engine('postgresql://postgres:wd123WD123@localhost/carrego')
    df_uploaded = pd.read_csv(filename, index_col=False)
    df2 = pd.read_sql_table(table_name='cars', con=engine)
    print(df2)
    return df_uploaded.to_sql(name='cars', con=engine, if_exists='append', index=False)
'''


@app.route('/Save_to_DB', methods=['GET', 'POST'])
def save_to_db():
    engine = create_engine('postgresql://postgres:wd123WD123@localhost/carrego')
    df2 = pd.read_sql_table(table_name='cars', con=engine)
    df_uploaded = pd.read_csv(filename, index_col=False)

    completed = []

    for row in df_uploaded['regonum']:

        if row in df2['regonum'].tolist():
            completed.append('Duplicated')
            
        else:
            df_uploaded.to_sql(name='cars', con=engine, if_exists='append', index=False)
            completed.append('Validated')
            df_uploaded['completed'] = completed
            
    return render_template('upload_results.htm', pd_table=df_uploaded.to_html())
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Data
from . import db
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)



@views.route('/upload')
@login_required
def upload():
    return render_template('upload.html', user=current_user)

@views.route('/success', methods=['POST'])
@login_required
def fileupload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        filedataframe = pd.read_csv(f.filename, encoding='latin1')
        smallerdf = pd.DataFrame(data=filedataframe.head(5))
        
        view_path = Path(r"C:\Users\Benjamin Cheung\projects\csv-test-calc\website\templates\view.html")
        existingdata = Data.query.filter_by(filename = f.filename).first()
        
        if not existingdata:
            new_data = Data(filename=f.filename, author=current_user.id)
            db.session.add(new_data)
            db.session.commit()
        else:
            flash('A file with this name already exists', category='error')
            return render_template('upload.html', user=current_user)
        return render_template('success.html', name=f.filename, user=current_user,
                               tables=[smallerdf.to_html(classes='data', header="true")])

@views.route('/view')
@login_required
def view():
    dfs = []
    data = Data.query.filter_by(author=current_user.id).all()
    for csv in data:
        newdf = pd.read_csv(csv.filename,encoding='latin1').head(5)
        dfs.append(newdf)
        
    
    return render_template('view.html', 
                           user=current_user, 
                           data=data, 
                           tables=[dataframe.to_html(classes='data', header='true') for dataframe in dfs]
                           )


@views.route('/delete/<id>')
@login_required
def delete(id):
    data = Data.query.filter_by(id=id).first()
    alldata = Data.query.filter_by(author=current_user.id).all()
    if not data:
        flash('File does not exist', category='error')
        return render_template('view.html', 
                        user=current_user, 
                        data=alldata, 
                        tables=[dataframe.to_html(classes='data', header='true') for dataframe in dfs]
                        )
    else:
        path = Path(r'C:/Users/Benjamin Cheung/projects/csv-test-calc', data.filename)
        os.remove(path)
        db.session.delete(data)
        db.session.commit()
        flash('File deleted', category='success')
        
    dfs = []
    rest = Data.query.filter_by(author=current_user.id).all()
    for csv in rest:
        newdf = pd.read_csv(csv.filename, encoding='latin1').head(5)
        dfs.append(newdf)
    return render_template('view.html', 
                            user=current_user, 
                            data=rest, 
                            tables=[dataframe.to_html(classes='data', header='true') for dataframe in dfs]
                            )

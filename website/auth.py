from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))  
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist. Please sign up.', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_pass = request.form.get('confirm_pass')
        password_upper = False
        email_exists = User.query.filter_by(email=email).first()
        user_exists = User.query.filter_by(username=username).first()

        for i in range(0, len(password)):
            if password[i].isupper():
                password_upper = True

        if email_exists:
            flash('Email is already in use. Please log in.', category='error')
        elif user_exists:
            flash('Username already in use.', category='error')
        elif password != confirm_pass:
            flash('Passwords do not match!', category='error')
        elif len(username) < 2:
            flash('Username is too short', category='error')
        elif len(password) < 6:
            flash('Password is too short.', category='error')
        elif password_upper == False:
            flash('Password must contain at least one capital letter', category='error')
        elif len(email) < 5:
            flash('Email is invalid.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created successfully', category='success')
            return redirect(url_for('views.home'))
    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.upload'))
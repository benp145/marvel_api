from os import stat
# from app import app, db
from . import bp as app
from app import db
from flask import render_template, url_for, redirect, request, flash
from datetime import date, datetime
from app.blueprints.auth.models import User
from flask_login import login_user, logout_user, current_user



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form.get('email')).first() is not None:
            flash('That email already belongs to a user. Please try again.', 'warning')
            return redirect(request.referrer)
        if request.form.get('password') != request.form.get('confirm_password'):
            flash('Passwords do not match. Please try again.', 'warning')
            return redirect(request.referrer)
        u = User(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=request.form.get('email'),
            password=request.form.get('password')
        )
        u.generate_password(u.password)
        db.session.add(u)
        db.session.commit()
        flash('User created successfully', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(email=request.form.get('email')).first()
        if u is not None and u.check_password(request.form.get('password')):
            login_user(u)
            flash('You have logged in successfully', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Incorrect username or password', 'danger')
            return redirect(request.referrer)
        # flash('You have logged in successfully', 'success')
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('User logged out succsessfully', 'info')
    return redirect(url_for('auth.login'))
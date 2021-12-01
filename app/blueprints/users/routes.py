from os import name, stat
from . import bp as app
from app import db
from flask import render_template, url_for, redirect, request, flash
from datetime import date, datetime
from app.blueprints.auth.models import User
from app.blueprints.characters.models import Character
from flask_login import login_user, logout_user, current_user

@app.route('/')
def home():

    context = {
        'users': User.query.order_by(User.date_created.desc()).all()
    }
    return render_template('users/index.html', **context)

@app.route('/<id>')
def user(id):
    current_u = None
    try:
        if id.isdigit():
            current_u = User.query.get(id)

            if current_u == None:
                raise ValueError(f'User {id} not found')
        else:
            raise ValueError(f'ID: {id} is not valid')
    except ValueError as e:
        flash(str(e), 'danger')
    context = {
        'user': current_u,
        'characters': Character.query.filter_by(user_id=id).order_by(Character.date_created.desc()).all()
    }
    return render_template('users/user.html', **context)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    u = User.query.get(current_user.get_id())
    context = {
        'characters': Character.query.filter_by(user_id=u.get_id()).order_by(Character.date_created.desc()).all()
        # 'posts': Post.query.filter_by(user=u).all()
    }
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not password and not confirm_password:
            u.first_name = f_name
            u.last_name = l_name
            u.email = email
            db.session.commit()
            flash('You have successfully updated your profile', 'info')
            return redirect(request.referrer)
        else:
            if password == confirm_password:
                u.first_name = f_name
                u.last_name = l_name
                u.email = email
                u.generate_password(password)
                db.session.commit()
                flash('You have successfully updated your profile', 'info')
                return redirect(request.referrer)
            else:
                flash('Your passwords do not match. try again', 'danger')
                return redirect(request.referrer)
            
    return render_template('users/profile.html', **context)

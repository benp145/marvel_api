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
        'characters': Character.query.order_by(Character.date_created.desc()).all()
    }
    return render_template('characters/index.html', **context)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if Character.query.filter_by(name=request.form.get('name')).first() is not None:
            flash('There is already a character under that name.', 'warning')
            return redirect(url_for('characters.home'))
        c = Character(
            name=request.form.get('name'),
            description=request.form.get('description'),
            comics_appeared_in=int(request.form.get('comics_appeared_in')),
            super_power=request.form.get('super_power'),
            user_id = current_user.get_id()
        )
        db.session.add(c)
        db.session.commit()
        flash('Character added!', 'success')
        return redirect(url_for('characters.home'))
    return render_template('characters/new.html')


@app.route('/<id>')
def char(id):
    current_char = None
    try:
        if id.isdigit():
            current_char = Character.query.get(id)

            if current_char == None:
                raise ValueError(f'Character {id} not found')
        else:
            raise ValueError(f'ID: {id} is not valid')
    except ValueError as e:
        flash(str(e), 'danger')
    context = {
        'char': current_char
    }
    return render_template('characters/char.html', **context)
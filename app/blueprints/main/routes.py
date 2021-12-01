from os import stat
# from app import app, db
from . import bp as app
from app import db
from flask import render_template, url_for, redirect, request, flash
from datetime import date, datetime
from app.blueprints.auth.models import User
from flask_login import login_user, logout_user, current_user

@app.route('/')
def home():
    return render_template('index.html')


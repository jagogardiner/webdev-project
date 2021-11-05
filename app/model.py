from . import db
from flask import redirect, flash, current_app, url_for
from flask_login import UserMixin, current_user
from functools import wraps

# Database class for a user
class User(db.Model, UserMixin):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    passwordHash = db.Column(db.String(500))
    name = db.Column(db.String(100))

# Database class for a hotel
class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20))
    capacity = db.Column(db.Integer)
    peakPrice = db.Column(db.Integer)
    offPeakPrice = db.Column(db.Integer)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.id == 1:
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.")
            return redirect('/')
        return wrap

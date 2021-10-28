from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    passwordHash = db.Column(db.String(500))
    name = db.Column(db.String(100))

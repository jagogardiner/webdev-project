from . import db
from flask_login import UserMixin
from functools import wraps


class User(db.Model, UserMixin):
    # Database class for a user
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    passwordHash = db.Column(db.String(500))
    name = db.Column(db.String(100))


class Hotel(db.Model):
    # Database class for a hotel
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20))
    standardCapacity = db.Column(db.Integer)
    doubleCapacity = db.Column(db.Integer)
    familyCapacity = db.Column(db.Integer)
    totalCapacity = db.Column(db.Integer)
    peakPrice = db.Column(db.Integer)
    offPeakPrice = db.Column(db.Integer)
    booking = db.relationship("Booking")


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))

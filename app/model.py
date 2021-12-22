from . import db
from flask_login import UserMixin

# TODO: Comment and refactor


class User(db.Model, UserMixin):
    # Database class for a user
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    passwordHash = db.Column(db.String(500))
    name = db.Column(db.String(100))
    booking = db.relationship("Booking", back_populates="user")


class Hotel(db.Model):
    # Database class for a hotel
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(20))
    standardCapacity = db.Column(db.Integer)
    doubleCapacity = db.Column(db.Integer)
    familyCapacity = db.Column(db.Integer)
    totalCapacity = db.Column(db.Integer)
    peakPrice = db.Column(db.Integer)
    offPeakPrice = db.Column(db.Integer)
    booking = db.relationship("Booking", back_populates="hotel")


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotel.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    room_type = db.Column(db.String(10))
    guests = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    price_pn = db.Column(db.Integer)
    transaction_date = db.Column(db.Date)
    booking_reference = db.Column(db.String(20))
    hotel = db.relationship("Hotel")
    user = db.relationship("User")

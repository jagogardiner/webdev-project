from . import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, UserMixin):
    # Database class for a user
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    passwordHash = db.Column(db.String(500))
    name = db.Column(db.String(100))
    user_type = db.Column(db.Integer)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)


class Hotel(db.Model, SerializerMixin):
    # Database class for a hotel
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(20))
    standardCapacity = db.Column(db.Integer)
    doubleCapacity = db.Column(db.Integer)
    familyCapacity = db.Column(db.Integer)
    totalCapacity = db.Column(db.Integer)
    peakPrice = db.Column(db.Integer)
    offPeakPrice = db.Column(db.Integer)


class Booking(db.Model, SerializerMixin):
    # Database class for a booking
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotel.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    room_type = db.Column(db.String(10))
    guests = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    transaction_date = db.Column(db.Date)
    booking_reference = db.Column(db.String(20))
    hotel = db.relationship("Hotel")
    user = db.relationship("User")

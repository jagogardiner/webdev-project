from flask import Blueprint, render_template, redirect, request, flash, current_app, url_for, abort
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.orm.session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from .model import User, Hotel, Booking
from app import db
from functools import wraps

auth = Blueprint('auth', __name__)


def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        return redirect(dest)
    except:
        return redirect(fallback)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.id == 1:
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.")
            return redirect('/')
    return wrap


@auth.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember-me') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.passwordHash, password):
            flash('Please check your login details and try again.')
            return redirect('/login')

        current_app.logger.info('Logging in')
        login_user(user, remember=remember)
        if(user.id == 1):
            return redirect('/admin')
        return redirect_dest(fallback=url_for('app.home'))

    # or:
    return render_template('login.html')


@auth.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        user = User.query.filter_by(email=email).first()
        # if this returns a user, then the email already exists in database
        if user:
            flash('Email address already exists!')
            return redirect('/signup')

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, passwordHash=generate_password_hash(
            password, method='sha256'), name=name)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('signup.html')


@auth.route("/member")
@login_required
def member_page():
    if(current_user.id == 1):
        return redirect('/admin')
    return render_template('member.html', name=current_user.name)


@auth.route("/admin")
@login_required
@admin_required
def admin_dash():
    return render_template('admin.html')


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('home.html')


@auth.route("/booking/<city>", methods=['POST', 'GET'])
@login_required
def booking(city):
    hotel = Hotel.query.filter_by(city=city).first_or_404()
    if request.method == 'POST':
        roomType = request.form.get('roomType')
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        guestAmount = request.form.get('guestAmount')
        price = request.form.get('inputTotalCost')
        transactionDate = request.form.get('transactionDate')

        currentHotel = db.session.query(
            Hotel).filter(Hotel.city == city).first()
        userId = current_user.id

        new_booking = Booking(room_type=roomType, start_date=startDate, end_date=endDate, guests=guestAmount,
                              hotel_id=currentHotel.id, user_id=userId, price_pn=price, transaction_date=transactionDate)

        # Add booking data to DB session
        db.session.add(new_booking)
        db.session.commit()

        return url_for('auth.successBooking', bookingId=new_booking.id)

    return render_template('booking.html', hotel=hotel)


@auth.route("/bookingSuccess/<bookingId>")
@login_required
def successBooking(bookingId):
    # Get booking details from ID.
    booking = Booking.query.filter_by(id=int(bookingId)).first()
    if(booking.user_id != current_user.id):
        # Abort if logged in user is mot the user assigned to the booking.
        abort(403)
    # Join Hotel object from Booking.
    hotel = db.session.query(Hotel).filter(
        Hotel.id == booking.hotel_id).first()

    return render_template('bookingSuccess.html', booking=booking, hotel=hotel)

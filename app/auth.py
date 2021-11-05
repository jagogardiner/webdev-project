from flask import Blueprint, render_template, redirect, request, flash, current_app, url_for
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .model import User, Hotel
from app import db

auth = Blueprint('auth', __name__)


def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except:
        return redirect(fallback)
    return redirect(dest_url)


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
        return redirect_dest(fallback=url_for('home'))

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
def admin_dash():
    if(current_user.id != 1):
        return redirect('/member')
    return render_template('admin.html')


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('home.html')


@auth.route("/booking/<city>")
@login_required
def booking(city):
    hotel = Hotel.query.filter_by(city=city).first_or_404()
    return render_template('booking.html', hotel=hotel)

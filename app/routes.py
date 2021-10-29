""" Flask website routes """
from flask import render_template, request
from .main import app


@app.route("/")
@app.route("/home")
def home():
    user = {'username': 'Jago'}
    return render_template('home.html', title='Home', user=user)


@app.route("/locations")
def locations():
    return render_template('locations.html')


@app.route("/header")
def renderHeader():
    return render_template("header.html")


@app.route("/footer")
def renderFooter():
    return render_template("footer.html")

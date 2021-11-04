""" Flask website routes """
from flask import render_template
from .main import app
from .model import Hotel


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/locations")
def locations():
    return render_template('locations.html', hotels=Hotel.query.all())


@app.route("/header")
def renderHeader():
    return render_template('header.html')


@app.route("/footer")
def renderFooter():
    return render_template('footer.html')

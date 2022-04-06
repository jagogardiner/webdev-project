""" Flask website routes """
from flask import render_template
from .main import app
from .model import Hotel


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", hotels=Hotel.query.all())


@app.route("/locations")
def locations():
    return render_template("locations.html", hotels=Hotel.query.all())


@app.route("/hotel/<city>")
def view_hotel(city):
    hotel = Hotel.query.filter_by(city=city).first_or_404()
    return render_template("hotel.html", hotel=hotel)


@app.route("/header")
def renderHeader():
    return render_template("header.html")


@app.route("/footer")
def renderFooter():
    return render_template("footer.html")

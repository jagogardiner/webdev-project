""" Flask website routes """
from datetime import datetime
from flask import render_template, request
from flask.json import jsonify
from .main import app
from .model import Hotel, Booking
from .costs import Costs


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


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


@app.route("/api/costs", methods=["POST"])
def cost_api():
    data = request.get_json()
    new_booking = Booking(
        room_type=data["room_type"],
        start_date=datetime.strptime(data["start_date"], "%Y-%m-%d"),
        end_date=datetime.strptime(data["end_date"], "%Y-%m-%d"),
        guests=0,
        hotel_id=data["hotel_id"],
        user_id=1,
        transaction_date=datetime.today(),
        booking_reference="",
        hotel=Hotel.query.filter_by(id=data["hotel_id"]).first_or_404(),
    )
    costs = Costs(new_booking)
    return jsonify(costs.__dict__), 200

from flask import Blueprint, jsonify, request, url_for
from .costs import Costs
from flask_login import login_required, current_user
from . import db
from .model import Booking, Hotel
from datetime import datetime
import random
import string

api = Blueprint("api", __name__)


@api.route("/api/costs", methods=["POST"])
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


@api.route("/api/newBooking", methods=["POST"])
@login_required
def api_make_booking():
    roomType = request.form.get("roomType")
    startDate = request.form.get("startDate")
    endDate = request.form.get("endDate")
    guestAmount = request.form.get("guestAmount")

    # Generate random booking reference
    bookingReference = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
    ).upper()

    new_booking = Booking(
        room_type=roomType,
        start_date=startDate,
        end_date=endDate,
        guests=guestAmount,
        hotel_id=1,
        user_id=current_user.id,
        transaction_date=datetime.now(),
        booking_reference=bookingReference,
    )

    # Add booking data to DB session
    db.session.add(new_booking)
    db.session.commit()

    return url_for("auth.successBooking", bookingId=new_booking.id)


@api.route("/api/bookingPrice", methods=["POST"])
@login_required
def api_booking_price():
    bookings = (
        db.session.query(Booking)
        .filter(current_user.id == Booking.user_id)
        .filter(Booking.id)
        .all()
    )
    dict = {}
    for row in bookings:
        cost = Costs(row)
        dict[row.__dict__["id"]] = cost.paid
    return jsonify(dict)

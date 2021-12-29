from flask import Blueprint, jsonify, request, current_app, send_file, abort
from .costs import Costs
from flask_login import login_required, current_user
from . import db
from .model import Booking, Hotel
from datetime import datetime
from .pdf import Receipt
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

    try:
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
    except Exception:
        return "Error", 500

    dict = new_booking.to_dict()
    # Add booking data to DB session
    db.session.add(new_booking)
    db.session.commit()

    return jsonify(dict)


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


@api.route("/api/hotelinfo", methods=["POST"])
def api_hotel_info():
    data = request.get_json()
    hotel = db.session.query(Hotel).filter(Hotel.id == data["hotel_id"]).one().to_dict()
    return jsonify(hotel)


@api.route("/api/invoice/<bookingId>")
@login_required
def getInvoice(bookingId):
    # Get booking details from ID.
    booking = Booking.query.filter_by(id=int(bookingId)).first()
    if booking.user_id != current_user.id:
        # Abort if logged in user is mot the user assigned to the booking.
        abort(403)
    receipt = Receipt(booking=booking)
    pdf = receipt.pdf
    path = current_app.config["CLIENT_PDF"] + booking.booking_reference + "-booking.pdf"
    pdf.output(path, dest="S")
    return send_file(path, environ=request.environ, as_attachment=True)

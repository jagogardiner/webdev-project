from flask import Blueprint, jsonify, request, current_app, send_file, abort
from .costs import Costs
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from . import db
from .model import Booking, Hotel, User
from datetime import datetime
from .pdf import Receipt
import random
import string

api = Blueprint("api", __name__)


@api.route("/api/costs", methods=["POST"])
def cost_api():
    """Returns all relative cost object information for a booking.

    Returns:
        JSON: Costs object as JSON.
    """
    # Get JSON recieved
    data = request.get_json()
    # Make a theoretical booking object
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
    # Make new costs object from this booking object
    costs = Costs(new_booking)
    return jsonify(costs.__dict__), 200


@api.route("/api/newbooking", methods=["POST"])
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
    db.session.close()

    return jsonify(dict), 200


@api.route("/api/member/bookingprices", methods=["POST"])
@login_required
def api_booking_price():
    """Returns price information for all member bookings as JSON.

    Returns:
        JSON: Booking ID and total paid
    """
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
    return jsonify(dict), 200


@api.route("/api/hotelinfo", methods=["POST"])
def api_hotel_info():
    """Returns information about a hotel in JSON form from a query.

    Returns:
        JSON: Hotel query object in JSON form.
    """
    data = request.get_json()
    hotel = db.session.query(Hotel).filter(Hotel.id == data["hotel_id"]).one().to_dict()
    return jsonify(hotel), 200


@api.route("/api/invoice/<booking_id>", methods=["POST"])
@login_required
def get_invoice(booking_id):
    """
    Returns a PDF invoice.
    Args:
        booking_id (str):

    Returns:
        PDF: Returns invoice in PDF form.
    """
    # Get booking details from ID.
    booking = Booking.query.filter_by(id=int(booking_id)).first()
    if booking.user_id != current_user.id:
        # Abort if logged in user is mot the user assigned to the booking.
        abort(403)
    receipt = Receipt(booking=booking)
    pdf = receipt.pdf
    path = current_app.config["CLIENT_PDF"] + booking.booking_reference + "-booking.pdf"
    pdf.output(path, dest="S")
    return send_file(path, environ=request.environ, as_attachment=True), 200


@api.route("/api/password", methods=["POST"])
@login_required
def change_password():
    old_password = request.form["oldPasswordInput"]
    new_password = request.form["newPasswordInput"]
    new_password_confirm = request.form["newPasswordConfirm"]

    if current_user.check_password(old_password):
        if new_password == new_password_confirm:
            user = db.session.query(User).filter(User.id == current_user.id).one()
            user.passwordHash = generate_password_hash(
                request.form["newPasswordConfirm"], method="sha256"
            )
            db.session.commit()
            db.session.close()
            return "OK", 200
    else:
        return "Bad password", 400

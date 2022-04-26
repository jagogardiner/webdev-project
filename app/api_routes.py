from flask import (
    Blueprint,
    jsonify,
    request,
    current_app,
    send_file,
    abort,
    redirect,
)

from .costs import Costs
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from . import db
from .model import Booking, Hotel
from datetime import datetime
from .pdf import Receipt
from .auth_routes import admin_required
import random
import string
import os

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
    hotelId = request.form.get("hotelId")

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
            hotel_id=hotelId,
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


@api.route("/api/invoice/<booking_id>", methods=["GET"])
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
    path = (
        current_app.root_path
        + current_app.config["CLIENT_PDF"]
        + booking.booking_reference
        + "-booking.pdf"
    )
    pdf.output(path, dest="S")
    return send_file(path, as_attachment=True), 200


@api.route("/api/password", methods=["POST"])
@login_required
def change_password():
    # API endpoint to change users password
    old_password = request.form["oldPasswordInput"]
    new_password = request.form["newPasswordInput"]
    new_password_confirm = request.form["newPasswordConfirm"]

    if current_user.check_password(old_password):
        if new_password == new_password_confirm:
            current_user.passwordHash = generate_password_hash(
                request.form["newPasswordConfirm"], method="sha256"
            )
            db.session.commit()
            db.session.close()
            return "OK", 200
    else:
        return "Bad password", 400


@api.route("/api/member/changename", methods=["POST"])
@login_required
def change_name():
    # API endpoint to change current users name
    current_user.name = request.form["newNameInput"]
    db.session.commit()
    db.session.close()
    return "OK", 200


@api.route("/api/admin/changehotelinfo", methods=["POST"])
@login_required
@admin_required
def change_hotel_info():
    """
    API endpoint to change hotel information.
    """
    city = request.form["cityval"]
    total_rooms = int(request.form["totalRoomsValue"])
    off_peak_price = int(request.form["offPeakPriceValue"])
    peak_price = int(request.form["peakPriceValue"])

    hotel = Hotel.query.filter_by(city=city).first()
    hotel.totalCapacity = total_rooms
    hotel.offPeakPrice = off_peak_price
    hotel.peakPrice = peak_price

    if (int(total_rooms) % 2) == 0:
        # if rooms are even, split 50/20/30
        hotel.doubleCapacity = total_rooms * 0.5
        hotel.familyCapacity = total_rooms * 0.2
        hotel.standardCapacity = total_rooms * 0.3
    else:
        # if rooms are odd, split 50/30/20 (-1 to account for rounding)
        total_rooms = total_rooms - 1
        hotel.doubleCapacity = total_rooms * 0.5
        hotel.familyCapacity = total_rooms * 0.2
        hotel.standardCapacity = total_rooms * 0.3
        # add one room to standard capacity.
        hotel.standardCapacity = hotel.standardCapacity + 1

    # get files from form
    if "imageFileUpload1" in request.files and not None:
        image_slot_1 = request.files["imageFileUpload1"]
        if not image_slot_1.filename == "":
            image_slot_1.save(
                os.path.join(
                    current_app.root_path,
                    "static/images/",
                    city,
                    "image1.jpg",
                )
            )
    if "imageFileUpload2" in request.files and not None:
        image_slot_2 = request.files["imageFileUpload2"]
        if not image_slot_2.filename == "":
            image_slot_2.save(
                os.path.join(
                    current_app.root_path,
                    "static/images/",
                    city,
                    "image2.jpg",
                )
            )
    if "imageFileUpload3" in request.files and not None:
        image_slot_3 = request.files["imageFileUpload3"]
        if not image_slot_3.filename == "":
            image_slot_3.save(
                os.path.join(
                    current_app.root_path,
                    "static/images/",
                    city,
                    "image3.jpg",
                )
            )

    db.session.commit()
    db.session.close()

    return redirect("/admin")


@api.route("/api/admin/addhotel", methods=["POST"])
@login_required
@admin_required
def add_hotel():
    """
    API endpoint to add a new hotel.
    """
    city = request.form["cityvalModal"]
    total_rooms = int(request.form["totalRoomsValueModal"])
    off_peak_price = int(request.form["offPeakPriceValueModal"])
    peak_price = int(request.form["peakPriceValueModal"])

    hotel = Hotel(
        city=city,
        totalCapacity=total_rooms,
        doubleCapacity=0,
        familyCapacity=0,
        standardCapacity=0,
        offPeakPrice=off_peak_price,
        peakPrice=peak_price,
    )

    if (int(total_rooms) % 2) == 0:
        # if rooms are even, split 50/20/30
        hotel.doubleCapacity = total_rooms * 0.5
        hotel.familyCapacity = total_rooms * 0.2
        hotel.standardCapacity = total_rooms * 0.3
    else:
        # if rooms are odd, split 50/30/20 (-1 to account for rounding)
        total_rooms = total_rooms - 1
        hotel.doubleCapacity = total_rooms * 0.5
        hotel.familyCapacity = total_rooms * 0.2
        hotel.standardCapacity = total_rooms * 0.3
        # add one room to standard capacity.
        hotel.standardCapacity = hotel.standardCapacity + 1

    os.mkdir(os.path.join(current_app.root_path, "static/images/", city))
    # get files from form
    if "imageFileUpload1Modal" in request.files and not None:
        image_slot_1 = request.files["imageFileUpload1Modal"]
        if not image_slot_1.filename == "":
            image_slot_1.save(
                os.path.join(
                    current_app.root_path,
                    "static/images/",
                    city,
                    "image1.jpg",
                )
            )
    if "imageFileUpload2Modal" in request.files and not None:
        image_slot_2 = request.files["imageFileUpload2Modal"]
        if not image_slot_2.filename == "":
            image_slot_2.save(
                os.path.join(
                    current_app.root_path,
                    "static/images/",
                    city,
                    "image2.jpg",
                )
            )
    if "imageFileUpload3Modal" in request.files and not None:
        image_slot_3 = request.files["imageFileUpload3Modal"]
        if not image_slot_3.filename == "":
            image_slot_3.save(
                os.path.join(
                    current_app.root_path,
                    "static/images/",
                    city,
                    "image3.jpg",
                )
            )

    db.session.add(hotel)
    db.session.commit()
    db.session.close()
    return redirect("/admin")


@api.route("/api/availability", methods=["POST"])
def check_availability():
    """
    Returns a JSON object with the availability of a room.
    Args:
        booking_id (str):

    Returns:
        JSON: Returns availability in JSON form.
    """
    data = request.get_json()
    hotel = db.session.query(Hotel).filter(Hotel.id == data["hotel_id"]).one().to_dict()
    room_type = data["room_type"]
    date_to = data["end_date"]
    date_start = data["start_date"]

    # get all bookings for the hotel + room type, before the end of the booking
    bookings = (
        db.session.query(Booking)
        .filter(Booking.hotel_id == hotel["id"])
        .filter(Booking.room_type == room_type)
        .filter(Booking.start_date >= date_start)
        .filter(Booking.end_date <= date_to)
        .count()
    )

    if bookings == 0:
        return jsonify({"available": True}), 200

    if room_type == "standard":
        if bookings >= hotel["standardCapacity"]:
            return jsonify({"available": False}), 200
    elif room_type == "double":
        if bookings >= hotel["doubleCapacity"]:
            return jsonify({"available": False}), 200
    elif room_type == "family":
        if bookings >= hotel["familyCapacity"]:
            return jsonify({"available": False}), 200

    # Must return true as the previous logic makes sure that we have rooms
    return jsonify({"available": True}), 200


@api.route("/api/cancelbooking", methods=["POST"])
@login_required
def cancel_booking():
    """
    API endpoint to cancel a booking.
    """
    booking_id = request.form["booking_id"]
    booking = Booking.query.filter_by(id=booking_id).first()
    if booking.user_id != current_user.id:
        # Abort if logged in user is not the user assigned to the booking.
        abort(403)
    db.session.delete(booking)
    db.session.commit()
    db.session.close()
    return "OK", 200

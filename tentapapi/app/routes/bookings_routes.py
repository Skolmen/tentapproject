from flask import jsonify, request, Blueprint
from app.extensions import db
from app.models.booking import Booking
from app.auth import api_key_required

bp = Blueprint('booking', __name__)

VALID_FIELDS = ['date', 'fm_person_id', 'em_person_id', 'fm_room', 'em_room', 'fm_notes', 'em_notes']

# Helper function to convert a Booking object to a dictionary
def booking_to_dict(booking):
    return {c.name: getattr(booking, c.name) for c in booking.__table__.columns}

# Returns all bookings
@bp.route('/bookings', methods=['GET'])
@api_key_required
def get_bookings():
    try:
        bookings = Booking.query.all()
        if not bookings:
            return jsonify({"message":"No bookings found"}), 204
        return jsonify([booking_to_dict(booking) for booking in bookings]), 200
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500

# Returns a booking by id
@bp.route('/bookings/<string:booking_date>', methods=['GET'])
@api_key_required
def get_booking(booking_date):
    try:
        # get booking by date
        booking = Booking.query.get(booking_date)
        if not booking:
            return jsonify({"message":"Booking not found"}), 404
        return jsonify(booking_to_dict(booking)), 200
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500
    
# Creates a new booking
@bp.route('/bookings', methods=['POST'])
@api_key_required
def create_booking():
    try:
        data = request.get_json()
        missing_fields = [field for field in VALID_FIELDS if field not in data]
        if missing_fields:
            return jsonify({"message":"Missing fields", "fields": ', '.join(missing_fields)}), 400
        new_booking = Booking(**data)
        db.session.add(new_booking)
        db.session.commit()
        return jsonify(booking_to_dict(new_booking)), 201
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500

# Updates a booking
@bp.route('/bookings/<string:booking_date>', methods=['PUT'])
@api_key_required
def update_booking(booking_date):
    try:
        data = request.get_json()
        missing_fields = [field for field in VALID_FIELDS if field not in data]
        if missing_fields:
            return jsonify({"message":"Missing fields", "fields": ', '.join(missing_fields)}), 400
        booking = Booking.query.get(booking_date)
        if not booking:
            return jsonify({"message":"Booking not found"}), 404
        for field, value in data.items():
            setattr(booking, field, value)
        db.session.commit()
        return jsonify(booking_to_dict(booking)), 200
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500

# Updates part of a booking
@bp.route('/bookings/<string:booking_date>', methods=['PATCH'])
@api_key_required
def patch_booking(booking_date):
    try:
        data = request.get_json()
        invalid_fields = [field for field in data if field not in VALID_FIELDS]
        if invalid_fields:
            return jsonify({"message":"Invalid fields", "fields": ', '.join(invalid_fields)}), 400
        booking = Booking.query.get(booking_date)
        if not booking:
            return jsonify({"message":"Booking not found"}), 404
        for field, value in data.items():
            setattr(booking, field, value)
        db.session.commit()
        return jsonify(booking_to_dict(booking)), 200
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500
        
#Deletes a booking
@bp.route('/bookings/<string:booking_date>', methods=['DELETE'])
@api_key_required
def delete_booking(booking_date):
    try:
        booking = Booking.query.get(booking_date)
        if not booking:
            return jsonify({"message":"Booking not found"}), 404
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message":"Booking deleted successfully"}), 204
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500



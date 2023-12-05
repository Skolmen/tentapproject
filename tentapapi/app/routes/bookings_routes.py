from flask import jsonify, request, Blueprint
from sqlalchemy.orm import aliased
from datetime import datetime

from app.extensions import db
from app.models.booking import Booking
from app.auth import api_key_required
from app.models.person import Person

bp = Blueprint('booking', __name__)

VALID_FIELDS = ['date', 'fm_person_id', 'em_person_id', 'fm_room', 'em_room', 'fm_notes', 'em_notes']

# Helper function to convert a Booking object to a dictionary
def booking_to_dict(booking, return_names=False):
    if return_names:
        keys = ['date', 'fm_room', 'em_room', 'fm_notes', 'em_notes', 'fm_person_name', 'em_person_name']
        booking_dict = dict(zip(keys, booking))
    else:
        booking_dict = {c.name: getattr(booking, c.name) for c in Booking.__table__.columns}
        
    if 'date' in booking_dict and booking_dict['date']:
        booking_dict['date'] = booking_dict['date'].strftime('%Y-%m-%d')
    return booking_dict

# Returns all bookings
@bp.route('/bookings', methods=['GET'])
@api_key_required
def get_bookings():
    try:
        with_names = request.args.get('with_names', 'false').lower() == 'true'
        start_date = request.args.get('start_date', None)
        
        print(start_date)
        
        # Define the common part of the query
        query = db.session.query(
            Booking.date,
            Booking.fm_room,
            Booking.em_room,
            Booking.fm_notes,
            Booking.em_notes
        )
        
        if with_names:
            personFM = aliased(Person)
            personEM = aliased(Person)    
            
            # Add the additional parts to the query
            query = query.add_columns(
                personFM.name.label('fm_person_name'),
                personEM.name.label('em_person_name')
            ).join(personFM, Booking.fm_person_id == personFM.person_id)\
            .join(personEM, Booking.em_person_id == personEM.person_id)
        else:
            # Add the additional parts to the query
            query = query.add_columns(
                Booking.fm_person_id,
                Booking.em_person_id
            )
        
        # If a start_date is provided, filter the bookings based on the start_date
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Booking.date >= start_date)
        
        bookings = query.all()
        
        if not bookings:
            return jsonify({"message":"No bookings found"}), 204
        return jsonify([booking_to_dict(booking, with_names) for booking in bookings]), 200
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500

# Returns a booking by id
@bp.route('/bookings/<string:booking_date>', methods=['GET'])
@api_key_required
def get_booking(booking_date):
    try:
        with_names = request.args.get('with_names', 'false').lower() == 'true'
        
        personFM = aliased(Person)
        personEM = aliased(Person)    
        
        query = db.session.query(
            Booking.date,
            Booking.fm_room,
            Booking.em_room,
            Booking.fm_notes,
            Booking.em_notes
        ).filter(Booking.date == booking_date)
        
        if with_names:
            query = query.add_columns(
                personFM.name.label('fm_person_name'),
                personEM.name.label('em_person_name')
            ).join(personFM, Booking.fm_person_id == personFM.person_id)\
            .join(personEM, Booking.em_person_id == personEM.person_id)
        else:
            query = query.add_columns(
                Booking.fm_person_id,
                Booking.em_person_id
            )
        
        booking = query.first()
        
        if not booking:
            return jsonify({"message":"Booking not found"}), 404
        return jsonify(booking_to_dict(booking, with_names)), 200
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500
    
# Creates a new booking
@bp.route('/bookings', methods=['POST'])
@api_key_required
def create_booking():
    try:
        print(request.get_json())
        data = request.get_json()
        missing_fields = [field for field in VALID_FIELDS if field not in data]
        if missing_fields:
            return jsonify({"message":"Missing fields", "fields": ', '.join(missing_fields)}), 400
        new_booking = Booking(**data)
        db.session.add(new_booking)
        db.session.commit()
        return jsonify(booking_to_dict(new_booking)), 201
    except Exception as e:
        print(e)
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



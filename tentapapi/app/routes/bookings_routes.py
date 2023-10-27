from flask import jsonify, request, Blueprint
from app.extensions import db
from app.models.booking import Booking
from app.auth import api_key_required
# Create a blueprint for the "booking" functionality
bp = Blueprint('booking', __name__)

@bp.route('/booking', methods=['GET'])
@api_key_required
def get_bookings():
    try:
        # Use SQLAlchemy to query the "Booking" table
        bookings = Booking.query.all()

        if not bookings:
            return "No bookings found", 204  # No content

        # Convert the SQLAlchemy objects to a list of dictionaries
        bookings_list = [
            {
                "id": booking.booking_id,
                "fm_person_id": booking.fm_person_id,
                "em_person_id": booking.em_person_id,
                "fm_room": booking.fm_room,
                "em_room": booking.em_room,
                "notes": booking.notes
            }
            for booking in bookings
        ]

        return jsonify(bookings_list), 200  # OK
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error

@bp.route('/booking/<int:booking_id>', methods=['GET'])
@api_key_required
def get_booking(booking_id):
    try:
        # Use SQLAlchemy to query the "Booking" table for a specific booking by ID
        booking = Booking.query.get(booking_id)

        if not booking:
            return "Booking not found", 404  # Not Found

        booking_data = {
            "id": booking.booking_id,
            "fm_person_id": booking.fm_person_id,
            "em_person_id": booking.em_person_id,
            "fm_room": booking.fm_room,
            "em_room": booking.em_room,
            "notes": booking.notes
        }

        return jsonify(booking_data), 200  # OK
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error

#Creates a new booking
@bp.route('/booking', methods=['POST'])
@api_key_required
def create_booking():
    try:
        data = request.get_json()

        # Check if all required fields are present in the JSON data
        required_fields = ['fm_person_id', 'em_person_id', 'fm_room', 'em_room', 'notes']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"Missing fields: {', '.join(missing_fields)}", 400  # Bad Request

        # Create a new Booking object with the provided data
        new_booking = Booking(
            fm_person_id=data['fm_person_id'],
            em_person_id=data['em_person_id'],
            fm_room=data['fm_room'],
            em_room=data['em_room'],
            notes=data['notes']
        )

        # Add the new booking to the database session and commit it
        db.session.add(new_booking)
        db.session.commit()

        # Return the newly created booking data
        return jsonify({
            "id": new_booking.booking_id,
            "fm_person_id": new_booking.fm_person_id,
            "em_person_id": new_booking.em_person_id,
            "fm_room": new_booking.fm_room,
            "em_room": new_booking.em_room,
            "notes": new_booking.notes
        }), 201  # Created
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error

#Updates a booking
@bp.route('/booking/<int:booking_id>', methods=['PUT'])
@api_key_required
def update_booking(booking_id):
    try:
        data = request.get_json()

        # Check if all required fields are present in the JSON data
        required_fields = ['fm_person_id', 'em_person_id', 'fm_room', 'em_room', 'notes']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"Missing fields: {', '.join(missing_fields)}", 400  # Bad Request

        # Use SQLAlchemy to query the booking for update
        booking = Booking.query.get(booking_id)

        if not booking:
            return "Booking not found", 404  # Not Found

        # Update the booking with the data from the JSON object
        booking.fm_person_id = data['fm_person_id']
        booking.em_person_id = data['em_person_id']
        booking.fm_room = data['fm_room']
        booking.em_room = data['em_room']
        booking.notes = data['notes']

        # Commit the changes to the database
        db.session.commit()

        # Return the updated booking data
        return jsonify({
            "id": booking.booking_id,
            "fm_person_id": booking.fm_person_id,
            "em_person_id": booking.em_person_id,
            "fm_room": booking.fm_room,
            "em_room": booking.em_room,
            "notes": booking.notes
        }), 200  # OK
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error

#Updates the rooms of a booking
@bp.route('/booking/<int:booking_id>', methods=['PATCH'])
@api_key_required
def patch_booking(booking_id):
    try:
        data = request.get_json()

        # Use SQLAlchemy to query the booking for update
        booking = Booking.query.get(booking_id)

        if not booking:
            return "Booking not found", 404  # Not Found

        # Update the fields that came with the JSON
        if 'fm_person_id' in data:
            booking.fm_person_id = data['fm_person_id']
        if 'em_person_id' in data:
            booking.em_person_id = data['em_person_id']
        if 'fm_room' in data:
            booking.fm_room = data['fm_room']
        if 'em_room' in data:
            booking.em_room = data['em_room']
        if 'notes' in data:
            booking.notes = data['notes']

        # Commit the changes to the database
        db.session.commit()

        # Return the updated booking data
        return jsonify({
            "id": booking.booking_id,
            "fm_person_id": booking.fm_person_id,
            "em_person_id": booking.em_person_id,
            "fm_room": booking.fm_room,
            "em_room": booking.em_room,
            "notes": booking.notes
        }), 200  # OK
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error

#Deletes a booking
@bp.route('/booking/<int:booking_id>', methods=['DELETE'])
@api_key_required
def delete_booking(booking_id):
    try:
        # Use SQLAlchemy to query the booking for deletion
        booking = Booking.query.get(booking_id)

        if not booking:
            return "Booking not found", 404  # Not Found

        # Use SQLAlchemy to delete the booking
        db.session.delete(booking)
        db.session.commit()

        return "", 204  # No Content
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error



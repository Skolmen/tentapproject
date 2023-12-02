from flask import request, jsonify, current_app, Blueprint
import requests

bp = Blueprint('bookings', __name__)

VALID_FIELDS = ['fm_person_id', 'em_person_id', 'fm_room', 'em_room', 'fm_notes', 'em_notes']

def get_api_details():
    API_LINK = current_app.config['TP_API'] + "bookings"
    API_KEY = current_app.config['TP_API_KEY']
    return API_LINK, API_KEY

# Get all bookings
@bp.route('', methods=['GET'])
def get_bookings():
    try:
        API_LINK, API_KEY = get_api_details()
        # Make the GET request with custom headers
        response = requests.get(API_LINK, headers={
            'X-API-Key': API_KEY
        })

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Parse the response JSON
            return jsonify({
                "data": data
            }), 200
        else:
            return jsonify({
                "response": response.json()
            }), response.status_code


    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500
    
# Get a booking by date
@bp.route('/<string:booking_date>', methods=['GET'])
def get_booking(booking_date):
    try:
        API_LINK, API_KEY = get_api_details()
        # Make the GET request with custom headers
        response = requests.get(API_LINK + "/" + str(booking_date), headers={
            'X-API-Key': API_KEY
        })

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Parse the response JSON
            return jsonify({
                "data": data
            }), 200
        else:            
            return jsonify({
                "response": response.json()
            }), response.status_code

    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500
    
# Creates a new booking
@bp.route('', methods=['POST'])
def create_booking():
    try:
        API_LINK, API_KEY = get_api_details()
        data = request.get_json()
        
        print(request.get_json())
        
        response = requests.post(API_LINK, json={
            'date': data['date'], 
            'fm_person_id': data['fm_person_id'],
            'em_person_id': data['em_person_id'],
            'fm_room': data['fm_room'],
            'em_room': data['em_room'],
            'fm_notes': data['fm_notes'],
            'em_notes': data['em_notes'],
        }, headers={
            'X-API-Key': API_KEY
        })
        
        if response.status_code == 201:
            return jsonify({
                "message": "Booking created successfully",
                "data": response.json(),
            }), 201
        else:
            return jsonify({
                "response": response.json()
            }), response.status_code
                    
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500
    
# Updates a booking a whole booking
@bp.route('/<string:booking_date>', methods=['PUT'])
def update_booking(booking_date):
    try:
        API_LINK, API_KEY = get_api_details()
        data = request.get_json()
        
        print(request.get_json())
        
        response = requests.put(API_LINK + "/" + booking_date, json={
            'date': data['date'],
            'fm_person_id': data['fm_person_id'],
            'em_person_id': data['em_person_id'],
            'fm_room': data['fm_room'],
            'em_room': data['em_room'],
            'fm_notes': data['fm_notes'],
            'em_notes': data['em_notes'],
        }, headers={
            'X-API-Key': API_KEY
        })
        
        if response.status_code == 200:
            return jsonify({
                "message": "Booking updated successfully",
                "data": response.json()
            }), 200
        else:
            return jsonify({
                "response": response.json()
            }), response.status_code
                    
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500
    
# Deletes a booking
@bp.route('/<string:booking_date>', methods=['DELETE'])
def delete_booking(booking_date):
    try:
        API_LINK, API_KEY = get_api_details()
        response = requests.delete(API_LINK + "/" + booking_date,
            headers={
                'X-API-Key': API_KEY
        })
        
        if response.status_code == 204:
            return jsonify({
                "message": "Booking deleted successfully",
            }), 204
        else:
            return jsonify({
                "response": response.json()
            }), response.status_code
                    
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500



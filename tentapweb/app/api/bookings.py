from flask import request, jsonify, current_app, Blueprint, has_request_context
import requests

from app.utils.helper_functions import getApiDetails

bp = Blueprint('bookings', __name__)

VALID_FIELDS = ['fm_person_id', 'em_person_id', 'fm_room', 'em_room', 'fm_notes', 'em_notes']

# Get all bookings
@bp.route('', methods=['GET'])
def get_bookings():
    try:
        with_names = request.args.get('with_names', 'false').lower() == 'true'
        start_date = request.args.get('start_date', None)

        query_params = []
        if with_names:
            query_params.append('with_names=true')
        if start_date:
            query_params.append(f'start_date={start_date}')

        endpoint = f"bookings?{'&'.join(query_params) if query_params else ''}"
        
        API_LINK, API_KEY = getApiDetails(endpoint)
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
        with_names = request.args.get('with_names', 'false').lower() == 'true'
        endpoint = f"bookings/{str(booking_date)}{'?with_names=true' if with_names else ''}"
        
        API_LINK, API_KEY = getApiDetails(endpoint)
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
    
# Creates a new booking
@bp.route('', methods=['POST'])
def create_booking():
    try:
        API_LINK, API_KEY = getApiDetails("bookings")
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
        API_LINK, API_KEY = getApiDetails("bookings")
        data = request.get_json()
                
        print
        
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
    
# Updates a booking a whole booking
@bp.route('/<string:booking_date>', methods=['PATCH'])
def update_booking_patch(booking_date):
    try:
        API_LINK, API_KEY = getApiDetails("bookings")
        data = request.get_json()
                
        print(data)        
                
        response = requests.patch(API_LINK + "/" + booking_date, json=data, headers={
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
        API_LINK, API_KEY = getApiDetails("bookings")
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



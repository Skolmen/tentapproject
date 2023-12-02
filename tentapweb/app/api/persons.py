from flask import request, jsonify, current_app, Blueprint
import requests

bp = Blueprint('persons', __name__)

def get_api_details(end_point):
    API_LINK = f"{current_app.config['TP_API']}{end_point}"
    API_KEY = current_app.config['TP_API_KEY']
    return API_LINK, API_KEY

@bp.route("", methods=['GET'])
def get_persons():
    try:
        API_LINK, API_KEY = get_api_details("person")
        
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
    
#Create a new person
@bp.route("", methods=['POST'])
def create_person():
    try:
        API_LINK, API_KEY = get_api_details("person")
        
        json_data = request.get_json()
        name = json_data['name']
        
        response = requests.post(API_LINK, json={
            'name': name,
        }, headers={
            'X-API-Key': API_KEY
        })
        
        
        
        if response.status_code == 201:
            return jsonify({
                "message": "Person created successfully",
                "data": response.json()
            }), 201
        else:
            return jsonify({
                "response": response.json()
            }), response.status_code
                    
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500
    
#Update a person
@bp.route("/<int:person_id>", methods=['PUT'])
def update_person(person_id):
    try:
        API_LINK, API_KEY = get_api_details("person")
        
        json_data = request.get_json()
        name = json_data['name']
        
        response = requests.put(f"{API_LINK}/{person_id}" , json={
            'name': name
        }, headers={
            'X-API-Key': API_KEY
        })
        
        if response.status_code == 200:
            return jsonify({
                "message": "Person updated successfully",
                "data": response.json()
            }), 200
        else:
            return jsonify({
                "response": response.json()
            }), response.status_code
        
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500
    
#Delete a person
@bp.route("/<int:person_id>", methods=['DELETE'])
def delete_person(person_id):
    try:               
        API_LINK, API_KEY = get_api_details("person")
        
        response = requests.delete(f"{API_LINK}/{person_id}",
            headers={
                'X-API-Key': API_KEY
        })
        
        if response.status_code == 204:
            return jsonify({
                "message": "Person deleted successfully",
            }), 204
        else:
            return jsonify({
                "response": response.json()
            }), response.status_code
        
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500
from flask import request, jsonify, current_app, Blueprint
import requests

bp = Blueprint('startpage', __name__)


def get_api_details():
    API_LINK = current_app.config['TP_API'] + "startpage"
    API_KEY = current_app.config['TP_API_KEY']
    return API_LINK, API_KEY

# Get startpage section
@bp.route('/<string:section>', methods=['GET'])
def get_startpage(section):
    try:
        API_LINK, API_KEY = get_api_details()
        # Make the GET request with custom headers
        response = requests.get(API_LINK + "/" + str(section), headers={
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
    
# Create a new startpage section
@bp.route('', methods=['POST'])
def create_startpage():
    try:
        API_LINK, API_KEY = get_api_details()
        data = request.get_json()
        section = data.get('section')
        content = data.get('content')
        
        # Make the POST request with custom headers
        response = requests.post(API_LINK, json={
            "section": section,
            "content": content
        }, headers={
            'X-API-Key': API_KEY
        })

        # Check if the request was successful (status code 201)
        if response.status_code == 201:
            data = response.json()  # Parse the response JSON
            return jsonify({
                "data": data
            }), 201
        else:            
            return jsonify({
                "response": response.json()
            }), response.status_code

    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500
    

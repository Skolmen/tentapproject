from flask import request, jsonify, current_app
import requests

from app.api import bp
from app.extensions import db

@bp.route("/subscribe", methods=["POST"])
def send_token_to_server():
    # Send token to application server
    try:        
        json_data = request.get_json()
        
        token = json_data['token']
        person_id = json_data['person_id']
        
        response = requests.post(current_app.config['TP_API'] + "messaging/token", json={
            'token': token,
            'person_id': person_id
        }, headers={
            'X-API-Key': current_app.config['TP_API_KEY']
        })
        
        if response.status_code == 200:
            return jsonify({
                "status": "subscribed",
            }), 200 # OK
        else:
            return f'Request failed with status code: {response.status_code}', response.status_code
        
    except requests.exceptions.RequestException as e:
        return f'Request error: {str(e)}', 500


@bp.route("/unsubscribe", methods=["POST"])
def remove_toke_from_server():
    try:
        json_data = request.get_json()
        
        token = json_data['token']
               
        response = requests.delete(current_app.config['TP_API'] + "messaging/token", json={
            'token': token
        }, headers={
            'X-API-Key': current_app.config['TP_API_KEY']
        })
        
        if response.status_code == 204:
            return jsonify({
                "status": "unsubscribed",
            }), 200 # OK
        else:
            return f'Request failed with status code: {response.status_code}', response.status_code
        
    except requests.exceptions.RequestException as e:
        return f'Request error: {str(e)}', 500
    
    
@bp.route("/updateToken", methods=["POST"])
def update_token():
    print("updateToken")
    try:
        json_data = request.get_json()
        print(json_data)
        old_token = json_data['old_token']
        new_token = json_data['new_token']
        
        response = requests.put(current_app.config['TP_API'] + "messaging/token", json={
            'old_token': old_token,
            'new_token': new_token
        }, headers={
            'X-API-Key': current_app.config['TP_API_KEY']
        })
        
        if response.status_code == 200:
            return jsonify({
                "status": "updated",
            }), 200
        else:
            return f'Request failed with status code: {response.status_code}', response.status_code
        
    except requests.exceptions.RequestException as e:
        return f'Request error: {str(e)}', 500

@bp.route("/persons", methods=['GET'])
def get_persons():
    try:
        # Make the GET request with custom headers
        response = requests.get(current_app.config['TP_API'] + "person", headers={
            'X-API-Key': current_app.config['TP_API_KEY']
        })

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Parse the response JSON
            return data
        else:
            return f'Request failed with status code: {response.status_code}', response.status_code

    except requests.exceptions.RequestException as e:
        return f'Request error: {str(e)}', 500
    
@bp.route("/updateNotificationSettings", methods=['POST'])
def update_notification_settings():
    try:
        json_data = request.get_json()
        token = json_data['token']
        settings = json_data['settings']
        
        response = requests.put(current_app.config['TP_API'] + "messaging/settings", json={
            'token': token,
            'settings': settings
        }, headers={
            'X-API-Key': current_app.config['TP_API_KEY']
        })
        
        if response.status_code == 200:
            return jsonify({
                "status": "updated",
            }), 200
        else:
            return f'Request failed with status code: {response.status_code}', response.status_code
        
    except requests.exceptions.RequestException as e:
        return f'Request error: {str(e)}', 500    


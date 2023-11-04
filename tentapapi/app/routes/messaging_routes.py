from flask import jsonify, request, Blueprint
from app.extensions import db
from app.models.fcm_token import FCMToken
from app.auth import api_key_required
from firebase_admin import messaging
from app.extensions import cred, default_app


# Create a blueprint for the "messaging" functionality
bp = Blueprint('messaging', __name__)

@bp.route('/token', methods=['POST'])
@api_key_required
def send_token():
    try:
        data = request.get_json()

        required_fields = ['token', 'person_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"Missing fields: {', '.join(missing_fields)}", 400
        
        new_token = FCMToken(
            token=data['token'],
            person_id=data['person_id']
        )        
        
        db.session.add(new_token)
        db.session.commit()
    
        return new_token.to_json(), 200  # OK
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error

#Deletes a token from the database
@bp.route('/token', methods=['DELETE'])
@api_key_required
def delete_token():
    try:
        data = request.get_json()
        
        required_fields = ['token']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"Missing fields: {', '.join(missing_fields)}", 400
                
        token = FCMToken.query.filter_by(token=data['token']).first()
        if not token:
            return "Token not found", 404  # Not Found
        
        db.session.delete(token)
        db.session.commit()
    
        return "Token removed", 204  # No Content
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error

#Gets all tokens from the database
@bp.route('/token', methods=['GET'])
@api_key_required
def get_tokens():
    try:
        tokens = FCMToken.query.all()
        return jsonify([token.to_json() for token in tokens]), 200  # OK
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500
    
#Notify all users with a token in the database
@bp.route('/notify', methods=['POST'])
@api_key_required
def notify_users():
    try:
        data = request.get_json()
        
        required_fields = ['title', 'body']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"Missing fields: {', '.join(missing_fields)}", 400
        
        tokens = FCMToken.query.all()
        
        if not tokens:
            return "No tokens found", 404  # Not Found
        
        # Send notification to all tokens
        for token in tokens:
            message = messaging.Message(
                data=data,
                token=token.token
            )
            
            response = messaging.send(message)
            print(f"Successfully sent message: {response}")
            
        
        return "Notification sent", 200  # OK
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500
from flask import request, jsonify
from app.models.api_key import ApiKey
from functools import wraps

def api_key_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')  # Assuming you pass the API key in a custom header

        if not provided_key:
            return jsonify({'message': 'API key is required'}), 401

        api_key = ApiKey.query.filter_by(api_key=provided_key, status='active').first()

        if not api_key:
            return jsonify({'message': 'Invalid API key'}), 401
        
        if request.method == 'GET' and api_key.permissions in ('read-only', 'read and write'):
            return func(*args, **kwargs)
        elif request.method in ('POST', 'PUT', 'PATCH', 'DELETE') and api_key.permissions == 'read and write':
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'Insufficient permissions'}), 403  # Forbidden

    return wrapper
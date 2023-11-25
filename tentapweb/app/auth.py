from flask import request, Response
from functools import wraps

def basic_auth_required(username, password):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not (auth.username == username and auth.password == password):
                return Response('Unauthorized <br/> <a href="/">Go back</a>', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            return f(*args, **kwargs)
        return decorated
    return decorator
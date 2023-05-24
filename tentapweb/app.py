from flask import Flask, request, jsonify, render_template, redirect, Response
from functools import wraps
import json
import sqlite3
import config
import re

ip = config.IP
port = config.PORT

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='')

def basic_auth_required(username, password):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not (auth.username == username and auth.password == password):
                return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            return f(*args, **kwargs)
        return decorated
    return decorator

# Route to serve the webpage
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to render the admin page
@app.route('/admin')
@basic_auth_required(config.USERNAME, config.PASSWORD)
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(host=ip, port=port)
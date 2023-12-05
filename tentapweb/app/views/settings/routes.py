from flask import render_template, current_app
import requests

from app.views.settings import bp
from app.utils.helper_functions import getApiDetails

# Route to serve the webpage
@bp.route('/')
def index():
    API_URL, API_KEY = getApiDetails('person')
    headers = {'X-API-Key': API_KEY}
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        persons = response.json()
    except requests.exceptions.RequestException as e:
        persons = []
    
    return render_template('settings/index.html', persons=persons)

@bp.route("/admin")
def admin_page():
    return render_template("settings/test.html")
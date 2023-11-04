from flask import render_template, current_app
import requests

from app.views.settings import bp

# Route to serve the webpage
@bp.route('/')
def index():
    headers = {'X-API-Key': current_app.config['TP_API_KEY']}
    try:
        response = requests.get('https://skolmen.asuscomm.com:56235/person', headers=headers)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        persons = response.json()
    except requests.exceptions.RequestException as e:
        persons = []
    
    return render_template('settings/index.html', persons=persons)

@bp.route("/admin")
def admin_page():
    return render_template("settings/test.html")
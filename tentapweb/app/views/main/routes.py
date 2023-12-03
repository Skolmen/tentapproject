from flask import render_template, current_app
import requests

from app.views.main import bp

def fetch_content(section):
    API_LINK = current_app.config['TP_API'] + "startpage"
    API_KEY = current_app.config['TP_API_KEY']

    response = requests.get(API_LINK + "/" + section, headers={
        'X-API-Key': API_KEY
    })

    if response.status_code == 200:
        data = response.json()  # Parse the response JSON
        return data["content"]

    return ""


# Route to serve the webpage
@bp.route('/')
def index():
    return render_template('index.html', information=fetch_content("INFORMATION"), priorities=fetch_content("PRIORITIES"))
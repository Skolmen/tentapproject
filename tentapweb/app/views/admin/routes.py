from flask import render_template, url_for, current_app
from app.auth import basic_auth_required
from config import USERNAME, PASSWORD
import requests

from app.views.admin import bp

@bp.route("/")
@basic_auth_required(USERNAME, PASSWORD)
def index():
    url_persons = url_for("admin.persons")
    url_bookings = url_for("admin.bookings")
    url_startpage = url_for("admin.startpage")
    return render_template("admin/index.html", url_persons=url_persons, url_bookings=url_bookings, url_startpage=url_startpage)

@bp.route("/persons")
@basic_auth_required(USERNAME, PASSWORD)
def persons():
    return render_template("admin/persons.html")

@bp.route("/bookings")
@basic_auth_required(USERNAME, PASSWORD)
def bookings():
    return render_template("admin/bookings.html")

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

@bp.route("/startpage")
@basic_auth_required(USERNAME, PASSWORD)
def startpage():
    information = fetch_content("INFORMATION")
    priorities = fetch_content("PRIORITIES")

    return render_template("admin/startpage.html", information=information, priorities=priorities)
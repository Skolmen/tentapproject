from flask import render_template, url_for, current_app
from app.auth import basic_auth_required
from config import USERNAME, PASSWORD

from app.views.admin import bp

from app.utils.helper_functions import fetchStartPageContent

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

@bp.route("/startpage")
@basic_auth_required(USERNAME, PASSWORD)
def startpage():
    information = fetchStartPageContent("INFORMATION")
    priorities = fetchStartPageContent("PRIORITIES")
    heading = fetchStartPageContent("HEADING")

    return render_template("admin/startpage.html", information=information, priorities=priorities, heading=heading)
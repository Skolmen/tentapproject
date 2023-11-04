from flask import render_template, url_for
from app.auth import basic_auth_required
from config import USERNAME, PASSWORD

from app.views.admin import bp

@bp.route("/")
@basic_auth_required(USERNAME, PASSWORD)
def index():
    url_persons = url_for("admin.persons")
    url_bookings = url_for("admin.bookings")
    return render_template("admin/index.html", url_persons=url_persons, url_bookings=url_bookings)

@bp.route("/persons")
@basic_auth_required(USERNAME, PASSWORD)
def persons():
    return render_template("admin/persons.html")

@bp.route("/bookings")
@basic_auth_required(USERNAME, PASSWORD)
def bookings():
    return render_template("admin/booking.html")
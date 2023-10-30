from flask import render_template
from app.auth import basic_auth_required
from config import USERNAME, PASSWORD

from app.views.admin import bp

@bp.route("/")
@basic_auth_required(USERNAME, PASSWORD)
def index():
    return render_template("admin/index.html")
from flask import render_template

from app.views.booking import bp

@bp.route("/")
def index():
    return render_template("booking/index.html")
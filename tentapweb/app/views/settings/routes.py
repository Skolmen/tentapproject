from flask import request, render_template
from flask_pywebpush import WebPush

from app.views.settings import bp

# Route to serve the webpage
@bp.route('/')
def index():
    return render_template('settings/index.html')

@bp.route("/admin")
def admin_page():
    return render_template("settings/test.html")
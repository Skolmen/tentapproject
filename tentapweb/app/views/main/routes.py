from flask import render_template

from app.views.main import bp

# Route to serve the webpage
@bp.route('/')
def index():
    return render_template('index.html')
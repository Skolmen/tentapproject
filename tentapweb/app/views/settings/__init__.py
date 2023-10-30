from flask import Blueprint

bp = Blueprint('settings', __name__)

from app.views.settings import routes
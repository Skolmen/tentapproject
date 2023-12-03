from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import persons, bookings, tokens, startpage

bp.register_blueprint(persons.bp, url_prefix="/persons")
bp.register_blueprint(bookings.bp, url_prefix="/bookings")
bp.register_blueprint(tokens.bp)
bp.register_blueprint(startpage.bp, url_prefix="/startpage")

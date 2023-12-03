from flask import Flask
from flask_cors import CORS

from config import CORS_WHITELIST
from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/*": {"origins": CORS_WHITELIST}})

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    
    #Bookings
    from app.routes.bookings_routes import bp as booking_bp    
    app.register_blueprint(booking_bp)

    #Persons     
    from app.routes.persons_routes import bp as persons_bp
    app.register_blueprint(persons_bp)
    
    #Token management
    from app.routes.messaging_routes import bp as messaging_bp
    app.register_blueprint(messaging_bp, url_prefix="/messaging")
    
    #Startpage
    from app.routes.startpage_routes import bp as startpage_bp
    app.register_blueprint(startpage_bp, url_prefix="/startpage")

    return app
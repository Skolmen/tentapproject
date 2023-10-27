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
    from app.routes.bookings_routes import bp as booking_bp    
    app.register_blueprint(booking_bp)
    
    from app.routes.persons_routes import bp as persons_bp
    app.register_blueprint(persons_bp)



    return app
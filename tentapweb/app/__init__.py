from flask import Flask

from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    
    #Booking
    from app.views.booking import bp as bp_booking
    app.register_blueprint(bp_booking, url_prefix="/booking")

    #Main
    from app.views.main import bp as bp_main
    app.register_blueprint(bp_main)

    #Admin
    from app.views.admin import bp as bp_admin
    app.register_blueprint(bp_admin, url_prefix="/admin")
    
    #Settings
    from app.views.settings import bp as bp_settings
    app.register_blueprint(bp_settings, url_prefix="/settings")
    
    #Settings
    from app.api import bp as bp_api
    app.register_blueprint(bp_api, url_prefix="/api")
    


    return app
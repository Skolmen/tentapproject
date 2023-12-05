from flask import Flask, send_from_directory, render_template 

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
        
    #FW config
    @app.route('/config/firebase-config')
    def fw_config():
        return send_from_directory('config', "firebase-config.js")
    
    #FCM Service Worker
    @app.route('/firebase-messaging-sw.js')
    def fcm_sw():
        return send_from_directory('static', "firebase-messaging-sw.js")

    #Icons
    @app.route('/icons/<path:filename>')
    def serve_icon(filename):
        return send_from_directory('static/icons', filename)
    
    #404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
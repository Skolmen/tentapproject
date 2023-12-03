from flask import jsonify, request, Blueprint
from app.extensions import db
from app.models.startpage import StartPageSections
from app.auth import api_key_required

bp = Blueprint('startpage', __name__)

# Get a specific startpage section
@bp.route('/<string:section>', methods=['GET'])
@api_key_required
def get_startpage(section):
    try:
        # Get the latest version of the startpage section with the highest version_id and latest version_date
        startpage_section = StartPageSections.query.filter_by(section=section).order_by(StartPageSections.version_id.desc(),
                                                                                        StartPageSections.version_date.desc()).first()
        if startpage_section is None:
            return jsonify({"message":"Not Found"}), 404
        
        return jsonify({"section": startpage_section.section, "content": startpage_section.content}), 200
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500
    

# Create a new startpage section
@bp.route('', methods=['POST'])
@api_key_required
def create_startpage():
    try:
        data = request.get_json()
        section = data.get('section')
        content = data.get('content')
        
        # Add new startpage section to database
        new_startpage = StartPageSections(section=section, content=content)
        db.session.add(new_startpage)
        db.session.commit()
        
        return jsonify({
            "message":"Startpage section created",
            "data": {
                "section": section,
                "content": content
            }
            }), 201
    except Exception as e:
        return jsonify({"message":"Internal Server Error", "error": str(e)}), 500   
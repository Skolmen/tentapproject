## NOT WORKING ##



from flask import jsonify, request, Blueprint

from database.database import get_db_connection
from tentapproject.tentapapi.app.utils import *
import mysql.connector

# Create a blueprint for the "person" functionality
priorities_bp = Blueprint('priorities', __name__)

@priorities_bp.route('/priorities', methods=['GET'])
def get_priorities():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT priority, text FROM priorities ORDER BY priority')
        priorities = cursor.fetchall()
        conn.close()

        priority_list = [{"priority": priority, "text": text} for priority, text in priorities]

        return jsonify(priority_list), 200  # OK, return the list of priorities
    except Exception as e:
        # Handle errors and return priorities_bp ropriate HTTP status codes
        return "Internal Server Error", 500  # Internal Server Error

# Creats a new prio  
@priorities_bp.route('/priorities', methods=['POST'])
def new_priority():
    try:
        data = request.get_json()

        # Check if all required fields are present in the JSON data
        required_fields = ['priority', 'text']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"Missing fields: {', '.join(missing_fields)}", 400  # Bad Request

        priority = data.get('priority')
        text = data.get('text')

        # Sanitize and validate the input text
        text = sanitize_and_validate_text(text)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the new priority into the database
        cursor.execute('INSERT INTO priorities (priority, text) VALUES (%s, %s)', (priority, text))
        conn.commit()

        # Get the ID of the newly inserted priority using cursor.lastrowid
        new_id = cursor.lastrowid

        # Fetch the newly created data using the retrieved ID
        cursor.execute('SELECT priority, text FROM priorities WHERE priority_id = %s', (new_id,))
        new_priority_data = cursor.fetchone()

        conn.close()

        if not new_priority_data:
            return "Priority not found after insertion", 404  # Not Found

        new_priority = {
            "priority_id": new_priority_data[0][0],
            "priority": new_priority_data[0][1],
            "text": new_priority_data[0][2]
        }

        return jsonify(new_priority), 201  # Created, return the newly added entry
    except mysql.connector.errors.IntegrityError as e:
        return "Priority with the same priority value already exists", 409  # Conflict
    except Exception as e:
        # Handle other errors and return priorities_bp ropriate HTTP status codes
        return "Internal Server Error", 500  # Internal Server Error

# Edits a prio
@priorities_bp.route('/priorities/<int:priority_id>', methods=['PUT'])
def update_priority(priority_id):
    try:
        data = request.get_json()

        # Check if all required fields are present in the JSON data
        required_fields = ['priority', 'text']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"Missing fields: {', '.join(missing_fields)}", 400  # Bad Request

        priority = data.get('priority')
        text = data.get('text')

        # Sanitize and validate the input text
        text = sanitize_and_validate_text(text)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the priority exists
        cursor.execute('SELECT priority_id FROM priorities WHERE priority_id = %s', (priority_id,))
        existing_priority = cursor.fetchone()

        if not existing_priority:
            return "Priority not found", 404  # Not Found

        cursor.execute('UPDATE priorities SET priority = %s, text = %s WHERE priority_id = %s', (priority, text, priority_id))

        conn.commit()

        # Fetch the updated priority data
        cursor.execute('SELECT priority_id, priority, text FROM priorities WHERE priority_id = %s', (priority_id,))
        updated_priority_data = cursor.fetchone()

        conn.close()

        if not updated_priority_data:
            return "Updated priority not found", 404  # Not Found

        updated_priority = {
            "priority_id": updated_priority_data[0][1],
            "priority": updated_priority_data[0][1],
            "text": updated_priority_data[0][1]
        }

        return jsonify(updated_priority), 200  # OK, return the updated priority
    except Exception as e:
        # Handle errors and return priorities_bp ropriate HTTP status codes
        return "Internal Server Error", 500  # Internal Server Error

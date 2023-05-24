from flask import Flask, jsonify, request
import re
import sqlite3
from sqlite3 import Connection
from flask_cors import CORS
import config

ip = config.IP
port = config.PORT
cors_whitelist = config.CORS_WHITELIST

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": cors_whitelist}})

DATABASE = config.DATABASE_LOCATION
connection_pool: Connection = None

# Help functions --------------------------------------

def get_connection() -> Connection:
    global connection_pool
    if connection_pool is None:
        connection_pool = sqlite3.connect(DATABASE)
    return connection_pool

def validate_booking_type(booking_type):
    valid_booking_types = ['FM', 'EM']
    return booking_type in valid_booking_types

def validate_value(value):
    pattern = r'^([A-Za-z]{1,2}\d{1,3}|[-]?)$'
    return re.match(pattern, value) is not None

# Routes ----------------------------------------------

# Custom error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    if request.path == '/':
        error_message = 'Error: You can\'t acces this page.'
        return error_message, 403
    else:
        # Handle other 404 errors
        return render_template('404.html'), 404

# Error_type = 0, unknown error
# Error_type = 1, invalid booking type only FM or EM
# Error_type = 2, invalid room name
@app.route('/update_booking', methods=['POST'])
def update_booking():
    try:
        data = request.get_json()
        date = data['date']
        booking_type = data['type']
        value = data['value']

        # Validate booking type
        if not validate_booking_type(booking_type):
            return jsonify({'success': False, 'error_type': 1, 'error': 'Fel bokningstyp! Endast FM eller EM tillåts.'}), 400

        # Validate value
        if not validate_value(value):
            return jsonify({'success': False, 'error_type': 2, 'error': 'Felaktig salsnamn!'}), 400

        conn = get_connection()
        cursor = conn.cursor()

        if booking_type == 'FM':
            cursor.execute("UPDATE bookings SET sal_fm = ? WHERE date = ?", (value, date))
        elif booking_type == 'EM':
            cursor.execute("UPDATE bookings SET sal_em = ? WHERE date = ?", (value, date))
        else:
            return jsonify({'success': False, 'error_type': 1, 'error': 'Fel bokningstyp! Endast FM eller EM tillåts.'}), 400

        conn.commit()
        cursor.close()

        return jsonify({'success': True})
    except Exception as e:
        print('Error updating value:', str(e))
        return jsonify({'success': False, 'error_type': 0, 'error': 'Ett fel upptod!'}), 500

# Route to handle the booking form submission
@app.route('/add_booking', methods=['POST'])
def add_booking():
    # Get the form data from the request
    data = request.get_json()
    date = data['date']
    person_fm = data['person_fm']
    person_em = data['person_em']
    sal_fm = data['sal_fm']
    sal_em = data['sal_em']

    try:
        # Store the data in the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (date, person_1, person_2, sal_fm, sal_em) VALUES (?, ?, ?, ?, ?)",
                       (date, person_fm, person_em, sal_fm, sal_em))
        conn.commit()

        # Close the cursor (returns connection to the pool) instead of closing the connection
        cursor.close()

        # Redirect the user back to the admin page
        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        # Handle the duplicate entry error
        error_message = "A booking for this date already exists."
        return jsonify({'success': False, 'error': error_message})

# Removes a booking
@app.route('/remove_booking', methods=['POST'])
def remove_booking():
    try:
        data = request.get_json()
        booking_id = data['id']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        conn.commit()

        cursor.close()

        return jsonify({'success': True})
    except Exception as e:
        print('Error removing booking:', str(e))
        return jsonify({'success': False})

# Returns all the bookings
@app.route('/get_bookings', methods=['GET'])
def get_bookings():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings ORDER BY date ASC")
        bookings = cursor.fetchall()
        cursor.close()

        # Convert bookings to a list of dictionaries
        booking_list = []
        for booking in bookings:
            booking_dict = {
                'id': booking[0],
                'date': booking[1],
                'person_1': booking[2],
                'person_2': booking[3],
                'sal_fm': booking[4],
                'sal_em': booking[5]
            }
            booking_list.append(booking_dict)

        return jsonify(booking_list)
    except Exception as e:
        print('Error fetching bookings:', str(e))
        return jsonify([])

# --------------------------------------------------------

if __name__ == '__main__':
    app.run(host=ip, port=port)
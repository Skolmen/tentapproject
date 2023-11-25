from flask import jsonify, request, Blueprint
from app.extensions import db
from app.models.person import Person
from app.auth import api_key_required

# Create a blueprint for the "person" functionality
bp = Blueprint('person', __name__)

@bp.route('/person', methods=['GET'])
@api_key_required
def get_persons():
    try:
        # Use SQLAlchemy to query the "Person" table
        persons = Person.query.all()

        if not persons:
            return "No persons found", 204  # No content

        persons_list = [{"person_id": person.person_id, "name": person.name} for person in persons]
        return jsonify(persons_list), 200  # OK
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error

#Gets a specfic person
@bp.route('/person/<int:person_id>', methods=['GET'])
@api_key_required
def get_person(person_id):
    try:
        # Use SQLAlchemy to query the specific person by their ID
        person = Person.query.get(person_id)

        if not person:
            return "Person not found", 404  # Not Found

        person_data = {
            "person_id": person.person_id,
            "person_name": person.name,
        }

        return jsonify(person_data), 200  # OK
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error

#Creates a new person
@bp.route('/person', methods=['POST'])
@api_key_required
def create_person():
    try:
        data = request.get_json()

        # Create a new Person object with the provided data
        new_person = Person(name=data['name'])

        is_valid, error_message = new_person.validate()
        if not is_valid:
            return error_message, 400
                
        new_person.sterlize()

        # Add the new person to the database session and commit it
        db.session.add(new_person)
        db.session.commit()

        # Return the newly created person data
        return jsonify({
            "person_id": new_person.person_id,
            "person_name": new_person.name,
        }), 201  # Created
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error

#Updates a person
@bp.route('/person/<int:person_id>', methods=['PUT'])
@api_key_required
def update_person(person_id):
    try:
        data = request.get_json()

        # Use SQLAlchemy to query the person for update
        person = Person.query.get(person_id)

        if not person:
            return "Person not found", 404  # Not Found

        # Update the person's data
        person.name = data['name']

        # Commit the changes to the database
        db.session.commit()

        # Return the updated person data
        return jsonify({
            "person_id": person.person_id,
            "person_name": person.name,
        }), 200  # OK
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error

#Delets a person
@bp.route('/person/<int:person_id>', methods=['DELETE'])
@api_key_required
def delete_person(person_id):
    try:
        # Use SQLAlchemy to query the person for deletion
        person = Person.query.get(person_id)

        if not person:
            return "Person not found", 404  # Not Found

        # Use SQLAlchemy to delete the person
        db.session.delete(person)
        db.session.commit()

        return "", 204  # No Content
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return "Internal Server Error", 500  # Internal Server Error


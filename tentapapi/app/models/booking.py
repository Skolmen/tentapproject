from app.extensions import db

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fm_person_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'))  # Define a foreign key
    em_person_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'))  # Define a foreign key
    fm_room = db.Column(db.String(10))
    em_room = db.Column(db.String(10))
    notes = db.Column(db.Text)

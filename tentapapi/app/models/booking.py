from app.extensions import db

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    date = db.Column(db.Date, primary_key=True)
    fm_person_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'))  
    em_person_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'))
    fm_room = db.Column(db.String(10))
    em_room = db.Column(db.String(10))
    fm_notes = db.Column(db.Text)
    em_notes = db.Column(db.Text)

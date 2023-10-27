from app.extensions import db

class Person(db.Model):
    __tablename__ = 'persons'
    
    person_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
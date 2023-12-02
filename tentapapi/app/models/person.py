import re
from app.extensions import db

class Person(db.Model):
    __tablename__ = 'persons'
    person_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def validate(self):
        if not self.name:
            return False, 'nameIsEmpty'
        if not re.match("^[A-Öa-ö-' ]+$", self.name):
            return False, 'containsIllegalChars'
        if len(self.name) > 50:
            return False, 'nameTooLong'
        return True, None

    def sterlize(self):
        self.name = self.name.strip()
    

        
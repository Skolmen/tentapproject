from app.extensions import db

class Person(db.Model):
    def __init__(self, name):
        self.name = name
        
    def validate(self):
        # Check that the name is not empty
        if not self.name:
            return False, 'nameIsEmpty'
        
        # Check that the name only contains letters A-Ö, a-ö, space, hyphen and apostrophe
        for letter in self.name:
            if not (letter.isalpha() or letter == ' ' or letter == '-' or letter == "'"):
                return False, 'containsIllegalChars'
        
        # Check that the name is not longer than 50 characters
        if len(self.name) > 50:
            return False, 'nameTooLong'
        
        return True, None
    
    def sterlize(self):
        #remove trailing and leading whitespace
        self.name = self.name.strip()
    
    __tablename__ = 'persons'
    person_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    

        
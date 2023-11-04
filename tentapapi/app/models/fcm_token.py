from app.extensions import db

class FCMToken(db.Model):
    __tablename__ = 'push_tokens'

    token = db.Column(db.Text, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'))
    timestamp = db.Column(db.DateTime, server_default=('CURRENT_TIMESTAMP'))
    
    def to_json(self):
        return {
            'token': self.token,
            'person_id': self.person_id
        }
from app.extensions import db

class PushSubscription(db.Model):
    __tablename__ = 'push-subscriptions'    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    subscription_json = db.Column(db.Text)
    endpoint = db.Column(db.Text)
    person_id = db.Column(db.Integer)
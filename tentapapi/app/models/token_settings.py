from app.extensions import db

class TokenSettings(db.Model):
    __tablename__ = 'notification_settings'

    token = db.Column(db.Text, db.ForeignKey('push_tokens.token'), primary_key=True)
    booking_reminder = db.Column(db.Boolean, default=False)
    todays_rooms_reminder = db.Column(db.Boolean, default=False)
    tomorrow_rooms_reminder = db.Column(db.Boolean, default=False)
    
    def to_json(self):
        return {
            'token': self.token,
            'booking_reminder': self.booking_reminder,
            'todays_rooms_reminder': self.todays_rooms_reminder,
            'tomorrow_rooms_reminder': self.tomorrow_rooms_reminder
        }
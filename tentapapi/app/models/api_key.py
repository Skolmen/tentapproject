from app.extensions import db

class ApiKey(db.Model):
    __tablename__ = 'api_keys'

    PERMISSION_TYPES = ('read-only', 'read and write')
    KEY_STATUS = ('active', 'disabled')

    api_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_key = db.Column(db.String(255), unique=True)
    status = db.Column(db.Enum(*KEY_STATUS))
    permissions = db.Column(db.Enum(*PERMISSION_TYPES))
    created_at = db.Column(db.DateTime, server_default=('CURRENT_TIMESTAMP'))
from app import db, login_manager
from datetime import datetime as dt, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import base64, os
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    token = db.Column(db.String, index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    characters = db.relationship('Character', backref='user')

    def get_token(self, expires_in=3600):
        now = dt.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds = 60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    @staticmethod
    def check_token(token):
        u = User.query.filter_by(token=token).first()
        if u is None or u.token_expiration < dt.utcnow():
            return None
        return u

    def revoke_token(self):
        self.token_expiration = dt.utcnow() - timedelta(seconds=1)

    def to_dict(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'character_count': len(self.characters)
        }
        return data

    def generate_password(self, real_password):
        self.password = generate_password_hash(real_password)

    def check_password(self, real_password):
        return check_password_hash(self.password, real_password)

@login_manager.user_loader
def get_user(user_id):
    return User.query.get(user_id)
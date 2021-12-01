from app import db
from datetime import datetime as dt

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    comics_appeared_in = db.Column(db.Integer)
    super_power = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        from app.blueprints.auth.models import User

        data = {
            'name': self.name,
            'description': self.description,
            'comics_appeared_in': self.comics_appeared_in,
            'super_power': self.super_power,
            'user': User.query.get(self.user_id).to_dict()
        }
        return data


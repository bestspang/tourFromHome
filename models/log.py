from db import db

class LogModel(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(DateTime, default=datetime.datetime.utcnow)
    # timestamp = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')
    ip = db.Column(db.String(80))

    def __init__(self, user_id, ip, timestamp=timestamp):
        self.timestamp = timestamp
        self.user_id = user_id
        self.ip = ip

    @classmethod
    def find_by_name(cls, user_id):
        #SELECT * FROM items WHERE nane=name LIMIT 1
        return cls.query.filter_by(user_id=user_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

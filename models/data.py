from db import db

class DataModel(db.Model):
    __tablename__ = 'datas'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80))
    humid = db.Column(db.Float(precision=2))
    temp = db.Column(db.Float(precision=2))
    timestamp = db.Column(db.DateTime())
    # created_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    # api = db.Column(db.String(80))

    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    node = db.relationship('NodeModel')

    def __init__(self, uuid, humid, temp, timestamp, node_id):
        self.timestamp = timestamp
        self.uuid = uuid
        self.humid = humid
        self.temp = temp
        self.node_id = node_id

    def json(self):
        return {'time': self.timestamp.strftime("%d-%m-%Y|%H:%M:%S"),
                'temp': self.temp,
                'humid': self.humid,
                'node_id': self.node_id}

    @classmethod
    def find_by_uuid(cls, uuid):
        # SELECT * FROM items WHERE nane=name LIMIT 1
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

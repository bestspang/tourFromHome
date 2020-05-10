from db import db

class NodeModel(db.Model):
    __tablename__ = 'nodes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    model = db.Column(db.String(80), nullable=False)
    uuid = db.Column(db.String(80), nullable=False, unique=True)

    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')
    datas = db.relationship('DataModel', lazy='dynamic')

    def __init__(self, uuid, name, model):
        self.uuid = uuid
        self.name = name
        self.model = model


    def json(self):
        return {'id': self.id, 'uuid': self.uuid, 'data': [data.json() for data in self.datas.all()]}


    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first() #SELECT * FROM items WHERE nane=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class ActivateModel(db.Model):
    __tablename__ = 'activates'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    node_id = db.Column(db.Integer(), db.ForeignKey('nodes.id', ondelete='CASCADE'))

    def __init__(self, user_id, node_id):
        self.user_id = user_id
        self.node_id = node_id

    def json(self):
        return {'user_id': self.user_id, 'node_id': self.node_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #SELECT * FROM items WHERE nane=name LIMIT 1

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

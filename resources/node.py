from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.node import NodeModel, ActivateModel

class Node(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('model',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )


    def get(self, uuid):
        node = NodeModel.find_by_uuid(uuid)
        if node:
            return node.json()
        return {'message': 'Item not found'}, 404


    def post(self, uuid):
        if NodeModel.find_by_uuid(uuid):
            return {"message": "An item with uuid '{}' already exists".format(uuid)}, 400

        data = Node.parser.parse_args()  # request.get_json() #force=True,silent=True
        node = NodeModel(uuid, **data)  # data['price'], data['store_id']
        try:
            node.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return node.json(), 201

    def delete(self, uuid):
        node = NodeModel.find_by_uuid(uuid)
        if node:
            node.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, uuid):
        data = Node.parser.parse_args()  # request.get_json()

        node = NodeModel.find_by_uuid(uuid)

        if node is None:
            node = NodeModel(uuid, data['price'], data['store_id'])
        else:
            node.price = data['price']

        node.save_to_db()

        return node.json()

class Activate(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('model',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )


    def get(self, uuid):
        node = ActivateModel.find_by_uuid(uuid)
        if node:
            return node.json()
        return {'message': 'Item not found'}, 404


    def post(self, uuid):
        if ActivateModel.find_by_uuid(uuid):
            return {"message": "An item with uuid '{}' already exists".format(uuid)}, 400

        data = Activate.parser.parse_args()  # request.get_json() #force=True,silent=True
        node = NodeModel(uuid, **data)  # data['price'], data['store_id']
        try:
            node.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return node.json(), 201

    def delete(self, uuid):
        node = Activate.find_by_uuid(uuid)
        if node:
            node.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, uuid):
        data = Activate.parser.parse_args()  # request.get_json()

        node = NodeModel.find_by_uuid(uuid)

        if node is None:
            node = NodeModel(uuid, data['price'], data['store_id'])
        else:
            node.price = data['price']

        node.save_to_db()

        return node.json()

class NodeList(Resource):
    def get(self):
        # [item.json() for item in ItemModel.query.all()]
        return {'nodes': list(map(lambda x: x.json(), NodeModel.query.all()))}

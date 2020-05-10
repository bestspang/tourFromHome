from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.log import LogModel

class Log(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('user',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('ip',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('timestamp',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, name):
        node = NodeModel.find_by_name(name)
        if node:
            return node.json()
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if LogModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        data = Log.parser.parse_args()  # request.get_json() #force=True,silent=True
        log = LogModel(name, **data)  # data['price'], data['store_id']
        try:
            log.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return log.json(), 201

    def delete(self, name):
        log = LogModel.find_by_name(name)
        if log:
            log.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Log.parser.parse_args()  # request.get_json()

        log = LogModel.find_by_name(name)

        if log is None:
            log = ItemModel(name, data['price'], data['store_id'])
        else:
            log.price = data['price']

        log.save_to_db()

        return log.json()


class LogList(Resource):
    def get(self):
        # [item.json() for item in ItemModel.query.all()]
        return {'items': list(map(lambda x: x.json(), NodeModel.query.all()))}

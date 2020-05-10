from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.data import DataModel
from models.node import NodeModel
from datetime import datetime


class Data(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('humid',
        type=float,
        required=True,
        help="This field cannot be left blank!"
        )
    parser.add_argument('temp',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('timestamp',
        type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'),
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('node_id',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, uuid):
        data = DataModel.find_by_uuid(uuid)
        if data:
            return data.json()
        return {'message': 'Item not found'}, 404

    def post(self, uuid):
        # node_id = NodeModel.find_by_uuid(uuid)
        data = Data.parser.parse_args()  # request.get_json() #force=True,silent=True
        data = DataModel(uuid, **data)  # data['price'], data['store_id']
        try:
            data.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return data.json(), 201

    def delete(self, uuid):
        data = DataModel.find_by_uuid(uuid)
        if data:
            data.delete_from_db()
        return {'message': 'Item deleted'}

class DataList(Resource):
    def get(self):
        # [item.json() for item in ItemModel.query.all()]
        return {'items': list(map(lambda x: x.json(), DataModel.query.all()))}

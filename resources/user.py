from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('email',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('confirmpass',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists!"}, 400
        if UserModel.find_by_email(data['email']):
            return {"message": "An email is already exists!"}, 400
        elif data['password'] != data['confirmpass']:
            return {"message": "passwords is not match!"}, 400
        #data['username'], data['password'],**data
        user = UserModel(data['username'], data['password'], data['email'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserList(Resource):
    def get(self):
        # [item.json() for item in ItemModel.query.all()]
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}

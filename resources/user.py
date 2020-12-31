from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        # Admin user only
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username("admin"):
            return {"message": "User with that username already exists."}, 400

        user = UserModel("admin", data["password"])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

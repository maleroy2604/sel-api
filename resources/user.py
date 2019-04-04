from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import jwt_required

BLANK_ERROR = "'{}' can't let be blank."
NOT_FOUND_ERROR = "'{}' not found."
DELETE_SUCCEFUL = "'{}' succefully delete. "
ERROR_INSERTING = "An error occurred while inserting the'{}'."


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help=BLANK_ERROR.format("username")
    )
    parser.add_argument(
        "password", type=str, required=True, help=BLANK_ERROR.format("password")
    )
    parser.add_argument(
        "email", type=str, required=True, help=BLANK_ERROR.format("email")
    )

    @classmethod
    def get(cls, id: int):
        user = UserModel.find_by_id(id)
        if user:
            return user.json(), 201
        return {"message": NOT_FOUND_ERROR.format("user")}, 404

    @classmethod
    @jwt_required
    def delete(cls, id: int):
        user = UserModel.find_by_id(id)
        if user:
            user.delete_from_db()
            return {"message": DELETE_SUCCEFUL.format("user")}
        return {"message": NOT_FOUND_ERROR.format("user")}, 404

    @jwt_required
    def put(self, id: int):
        data = User.parser.parse_args()
        user = UserModel.find_by_id(id)
        if user:
            user.username = data["username"]
            user.password = data["password"]
            user.email = data["email"]
            try:
                user.save_to_db()
                return user.json(), 201
            except:
                return {"message": ERROR_INSERTING.format("user")}

        return {"message": NOT_FOUND_ERROR.format("user")}, 404


class UserList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return {"users": [user.json() for user in UserModel.find_all()]}

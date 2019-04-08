from flask_restful import Resource
from flask import request
from models.user import UserModel
from flask_jwt_extended import jwt_required
from schemas.user import UserSchema

NOT_FOUND_ERROR = "'{}' not found."
DELETE_SUCCEFUL = "'{}' succefully delete. "
ERROR_INSERTING = "An error occurred while inserting the'{}'."

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


class User(Resource):
    @classmethod
    def get(cls, id: int):
        user = UserModel.find_by_id(id)
        if user:
            return user_schema.dump(user), 201
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
        try:
            user_data = user_schema.load(request.get_json(), instance=UserModel())
        except ValidationError as err:
            return err.messages, 400
        user = UserModel.find_by_id(id)
        if user:
            user.username = user_data.username
            user.password = user_data.password
            user.email = user_data.email
            try:
                user.save_to_db()
                return user_schema.dump(user), 201
            except:
                return {"message": ERROR_INSERTING.format("user")}

        return {"message": NOT_FOUND_ERROR.format("user")}, 404


class UserList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return {"users": user_list_schema.dump(UserModel.find_all())}

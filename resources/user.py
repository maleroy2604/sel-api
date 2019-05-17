from flask_restful import Resource
from flask import request
from models.user import UserModel
from models.exchange import ExchangeModel
from flask_jwt_extended import jwt_required
from schemas.user import UserSchema
from libs.strings import gettext
from security import check_encrypted_password, encrypt_password

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, id: int):
        user = UserModel.find_by_id(id)
        if user:
            return user_schema.dump(user), 201
        return {"message": gettext("not_found_error").format("user")}, 404

    @classmethod
    @jwt_required
    def delete(cls, id: int):
        user = UserModel.find_by_id(id)
        if user:
            user.delete_from_db()
            return {"message": gettext("deleted_succefuly").format("user")}
        return {"message": gettext("not_found_error").format("user")}, 404

    @jwt_required
    def put(self, id: int):
        user_data = user_schema.load(request.get_json(), instance=UserModel())
        user = UserModel.find_by_id(id)
        if user:
            if user_data.password and user_data.confirmpassword:
                if user_data.password != user_data.confirmpassword:
                    user.password = encrypt_password(user_data.password)
            if user.username != user_data.username:
                user.username = user_data.username
                ExchangeModel.change_ownername_exchange(user.id, user.username)
            if user.email != user_data.email:
                user.email = user_data.email
            try:
                user.save_to_db()
                return user_schema.dump(user), 201
            except:
                return {"message": gettext("error_inserting").format("user")}, 500
            return {"message": gettext("error_password").format("password")}, 500
        return {"message": gettext("not not_found_error").format("user")}, 404


class UserList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return {"users": user_list_schema.dump(UserModel.find_all())}

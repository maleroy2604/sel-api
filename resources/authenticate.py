from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel
from resources.user import UserSchema
from security import check_encrypted_password
from libs.strings import gettext

user_schema = UserSchema()


class Authenticate(Resource):
    @classmethod
    def post(cls):
        try:
            data = user_schema.load(request.get_json(), instance=UserModel())
        except ValidationError as err:
            return err.messages, 400
        user = UserModel.find_by_username(data.username)
        if user and check_encrypted_password(data.password, user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return (
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user_schema.dump(user),
                },
                200,
            )

        return {"message": gettext("invalid_credentials")}, 401

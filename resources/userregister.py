from flask_restful import Resource
from flask import request
from resources.user import UserModel, UserSchema
from flask_jwt_extended import create_access_token, create_refresh_token
from security import encrypt_password

user_schema = UserSchema()


class UserRegister(Resource):
    def post(self):
        user = user_schema.load(request.get_json())
        if UserModel.find_by_username(user.username):
            return {"message": gettext("already_exists").format("User")}, 400
        if user.password != user.confirmpassword:
            return (
                {
                    "message": gettext("has_to_be_equals").format(
                        "password", "confirmpassword"
                    )
                },
                400,
            )

        user.confirmpassword = ""
        user.password = encrypt_password(user.password)
        user.save_to_db()
        user = UserModel.find_by_username(user.username)
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return (
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user_schema.dump(user),
            },
            201,
        )

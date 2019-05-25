from flask_restful import Resource
from flask import request
from resources.user import UserModel, UserSchema
from flask_jwt_extended import create_access_token, create_refresh_token
from security import encrypt_password
import re
from libs.strings import gettext

user_schema = UserSchema()


class UserRegister(Resource):
    def post(self):
        user = user_schema.load(request.get_json())
        regex_password = "(?=\D*\d)(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])[A-Za-z0-9]{4,}$"
        regex_username = "[a-z0-9]{4,}$"
        regex_email = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"

        if not re.match(regex_username, user.username):
            return {"message": gettext("bad_format").format("username")}, 400
        if re.match(regex_password, user.password) is not None:
            return {"message": gettext("bad_format").format("password")}, 400
        if not re.match(regex_email, user.email):
            return {"message": gettext("bad_format").format("email")}, 400
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

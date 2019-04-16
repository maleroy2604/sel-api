from flask_restful import Resource
from flask import request
from resources.user import UserModel, UserSchema
from flask_jwt_extended import create_access_token, create_refresh_token
from security import encrypt_password

ALREADY_EXISTS = "'{}' with this name already exists."
HAS_TO_BE_EQUALS = " '{}' and '{}' has to be the same. "

user_schema = UserSchema()


class UserRegister(Resource):
    def post(self):
        user = user_schema.load(request.get_json())
        if UserModel.find_by_username(user.username):
            return {"message": ALREADY_EXISTS.format("User")}, 400
        if user.password != user.confirmpassword:
            return (
                {"message": HAS_TO_BE_EQUALS.format("password", "confirmpassword")},
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

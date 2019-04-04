from flask_restful import Resource, reqparse
from resources.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token
from security import encrypt_password

BLANK_ERROR = "'{}' can't let be blank."
ALREADY_EXISTS = "'{}' with this name already exists."
HAS_TO_BE_EQUALS = " '{}' and '{}' has to be the same. "


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help=BLANK_ERROR.format("username")
    )
    parser.add_argument(
        "password", type=str, required=True, help=BLANK_ERROR.format("password")
    )
    parser.add_argument(
        "confirmpassword",
        type=str,
        required=True,
        help=BLANK_ERROR.format("confirmpassword"),
    )
    parser.add_argument(
        "email", type=str, required=True, help=BLANK_ERROR.format("email")
    )

    @classmethod
    def post(cls):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message": ALREADY_EXISTS.format("User")}, 400
        if data["password"] != data["confirmpassword"]:
            return (
                {"message": HAS_TO_BE_EQUALS.format("password", "confirmpassword")},
                400,
            )

        user = UserModel(
            data["username"], encrypt_password(data["password"]), data["email"]
        )
        user.save_to_db()
        user = UserModel.find_by_username(data["username"])
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return (
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user.json(),
            },
            201,
        )

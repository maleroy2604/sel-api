from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel
from security import check_encrypted_password

#private var
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                           type = str,
                           required = True,
                           help = "Username required."
                           )
_user_parser.add_argument('password',
                           type = str,
                           required = True,
                           help = "Password required."
                           )

class Authenticate(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and check_encrypted_password(data['password'], user.password):
            access_token = create_access_token(identity = user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return{
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.json()
            }, 200

        return {'message': 'Invalid credentials'}, 401

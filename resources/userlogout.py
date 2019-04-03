from flask_restful import Resource
from flask_jwt_extended import(create_access_token,
                               create_refresh_token,
                               jwt_refresh_token_required,
                               get_jwt_identity,
                               jwt_required,
                               get_raw_jwt
                               )
from blacklist import BLACKLIST

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}, 200

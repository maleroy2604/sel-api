from flask_restful import Resource, reqparse
from resources.user import UserModel
from flask_jwt_extended import(create_access_token,
                               create_refresh_token,
                               jwt_refresh_token_required,
                               get_jwt_identity
)

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token =  create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200

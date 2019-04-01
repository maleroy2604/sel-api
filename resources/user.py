from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import jwt_required

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = "Username required"
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = "Password required"
    )
    parser.add_argument('email',
        type = str,
        required = True,
        help = "email required"
    )

    @classmethod
    def get(cls, id):
        user = UserModel.find_by_id(id)
        if user:
            return user.json(),201
        return {'message': "User not found"}, 404

    @classmethod
    @jwt_required
    def delete(cls, id):
        user = UserModel.find_by_id(id)
        if user:
            user.delete_from_db()
            return {'message': "User succefully deleted"}
        return {'message': "User not found"}, 404


    @jwt_required
    def put(self, id):
        data = User.parser.parse_args()
        user = UserModel.find_by_id(id)
        if user:
            self.username = data['username']
            self.password = data['password']
            self.email = data['email']
            try:
                user.save_to_db()
                return user.json(), 201
            except:
                return{'message': "An error occurred while inserting the user"}

        return {'message': "User not found"}, 404

class UserList(Resource):
    @jwt_required
    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}

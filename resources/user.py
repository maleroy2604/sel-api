import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt import jwt_required

class User(Resource):
    parser = reqparse.RequestParser()
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
    parser.add_argument('counterhours',
        type = int
    )

    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return user.json(),201
        return {'message': "User not found"}, 404

    def post(self, username):
        if UserModel.find_by_username(username):
            return {'message': "User already exists."}, 400

        data = User.parser.parse_args()
        user = UserModel(username, data['password'],  data['email'])
        user.save_to_db()
        user = UserModel.find_by_username(username)

        return user.json() , 201

    @jwt_required()
    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()
            return {'message': "User succefully deleted"}
        return {'message': "User not found"}, 404

    @jwt_required()
    def put(self, username):
        data = User.parser.parse_args()
        user = UserModel.find_by_username(username)
        if user:
            user.password = data['password']
            user.email = data['email']
            user.counterHours = data['counterhours']
            try:
                user.save_to_db()
                return user.json(), 201
            except:
                return{'message': "An error occurred while inserting the user"}

        return {'message': "User not found"}, 404

class UserList(Resource):
    @jwt_required()
    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}

import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.message import MessageModel

class Message(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('message',
        type = str,
        required = True,
        help = "message is required"
    )
    parser.add_argument('sender',
        type = int,
        required = True,
        help = "sender is required"
    )
    parser.add_argument('exchange_id',
        type = int,
        required = True,
        help = "exchangeid is required"
    )

    @jwt_required()
    def post(self, id):
        data = Message.parser.parse_args()
        message = MessageModel(**data)
        try:
            message.save_to_db()
            #message.send_to_recipients()
        except:
            return {'message':"An error occurred inserting message"}, 500
        return message.json(), 201

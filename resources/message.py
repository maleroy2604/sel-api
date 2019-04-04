import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.message import MessageModel

BLANK_ERROR = "'{}' can't let be blank."
ERROR_INSERTING = "An error occurred while inserting the'{}'."


class Message(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "message", type=str, required=True, help=BLANK_ERROR.format("message")
    )
    parser.add_argument(
        "sender", type=int, required=True, help=BLANK_ERROR.format("sender")
    )
    parser.add_argument(
        "exchange_id", type=int, required=True, help=BLANK_ERROR.format("exchange_id")
    )

    @classmethod
    @jwt_required
    def post(cls, id: int):
        data = Message.parser.parse_args()
        message = MessageModel(**data)
        try:
            message.save_to_db()
            message.send_to_recipients()
        except:
            return {"message": ERROR_INSERTING.format("message")}, 500
        return message.json(), 201

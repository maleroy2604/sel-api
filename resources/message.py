import sqlite3
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.message import MessageModel
from schemas.message import MessageSchema
from flask import request

message_schema = MessageSchema()


class Message(Resource):
    @classmethod
    @jwt_required
    def post(cls, id: int):
        message = message_schema.load(request.get_json(), instance=MessageModel())
        try:
            message.save_to_db()
            return message_schema.dump(message), 201
        except:
            return ({"message": gettext("message_posted_sucefuly")}, 500)

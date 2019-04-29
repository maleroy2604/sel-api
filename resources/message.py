import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.message import MessageModel
from schemas.message import MessageSchema
from libs.strings import gettext

message_schema = MessageSchema()


class Message(Resource):
    @classmethod
    @jwt_required
    def post(cls, id: int):
        message = message_schema.load(request.get_json())
        try:
            message.save_to_db()
            message.send_to_recipients()
        except:
            return {"message": gettext("error_inserting")}, 500
        return message_schema.dump(message), 201

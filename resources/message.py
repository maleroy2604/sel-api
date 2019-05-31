import sqlite3
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.message import MessageModel
from models.exchange import ExchangeModel
from schemas.message import MessageSchema
from flask import request
from libs.strings import gettext

message_schema = MessageSchema()
message_schema_list = MessageSchema(many=True)


class Message(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        message = message_schema.load(request.get_json(), instance=MessageModel())
        # if message.senderId != get_jwt_identity():
        # return {"message": gettext("not_allow")}, 500
        try:
            message.save_to_db()
            return message_schema_list.dump(
                MessageModel.find_all_messages_by_exchange_id(message.exchangeId)
            )
        except:
            return ({"message": gettext("message_posted_sucefuly")}, 500)


class MessageList(Resource):
    @jwt_required
    def get(cls, id: int):
        exchange = ExchangeModel.find_by_id(id)
        return message_schema_list.dump(
            MessageModel.find_all_messages_by_exchange_id(id)
        )

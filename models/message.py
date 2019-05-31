from db import db
from typing import List


class MessageModel(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(256), nullable=False)
    avatarUrl = db.Column(db.String(256))

    exchangeId = db.Column(db.Integer, db.ForeignKey("exchanges.id"), nullable=False)
    exchange = db.relationship("ExchangeModel")

    senderId = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    sender = db.relationship("UserModel")

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all_messages_by_id(cls, id: int) -> List:
        return cls.query.filter_by(senderId=id)

    @classmethod
    def find_all_messages_by_exchange_id(cls, id: int) -> List:
        return cls.query.filter_by(exchangeId=id)

    @classmethod
    def change_avatar_url_messages(cls, user_id: int, avatarurl: str) -> List:
        for message in MessageModel.find_all_messages_by_id(user_id):
            message.avatarUrl = avatarurl
            message.save_to_db()

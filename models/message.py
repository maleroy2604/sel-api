from db import db
from flask_restful import marshal
from models.exchangeocurence import ExchangeOcurenceModel
from models.user import UserModel

# from models.configfields import user_fields


class MessageModel(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(80))

    exchangeId = db.Column(db.Integer, db.ForeignKey("exchanges.id"))
    exchange = db.relationship("ExchangeModel")

    sender = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def send_to_recipients(self) -> None:
        exchangeOcurences = ExchangeOcurenceModel.find_by_exchange_id(self.exchangeId)
        users = UserModel.find_participants(exchangeOcurences)
        for user in users:
            self.users_recipient.append(user)
        db.session.commit()

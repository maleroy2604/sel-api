from db import db


class MessageModel(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(256), nullable=False)

    exchangeId = db.Column(db.Integer, db.ForeignKey("exchanges.id"), nullable=False)
    exchange = db.relationship("ExchangeModel")

    senderId = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    sender = db.relationship("UserModel")

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

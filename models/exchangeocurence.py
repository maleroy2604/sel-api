from db import db
from models.user import UserModel
from typing import List


class ExchangeOcurenceModel(db.Model):
    __tablename__ = "exchangeocurence"

    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.Integer)
    participantName = db.Column(db.String(30))

    exchangeId = db.Column(db.Integer, db.ForeignKey("exchanges.id"), nullable=False)
    exchange = db.relationship("ExchangeModel")

    participantId = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    participant = db.relationship("UserModel")

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id: int) -> List:
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_exchange_id(cls, exchangeId: int) -> List:
        return cls.query.filter_by(exchangeId=exchangeId).all()

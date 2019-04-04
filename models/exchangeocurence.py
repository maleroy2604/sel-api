from db import db
from models.user import UserModel
from typing import Dict, List, Union

ExchangeOcurenceJSON = Dict[str, Union[str, int]]


class ExchangeOcurenceModel(db.Model):
    __tablename__ = 'exchangeocurence'

    id = db.Column(db.Integer, primary_key=True)
    validateUser = db.Column(db.Integer)
    hours = db.Column(db.Integer)

    exchangeId = db.Column(db.Integer, db.ForeignKey('exchanges.id'))
    exchange = db.relationship('ExchangeModel')

    participantId = db.Column(db.Integer, db.ForeignKey('users.id'))
    participant = db.relationship('UserModel')

    def __init__(self, exchange_id: int, participant_id: int):
        self.exchangeId = exchange_id
        self.participantId = participant_id
        self.hours = 0

    def json(self) -> ExchangeOcurenceJSON:
        return {'id': self.id,
                    #'validateuser': self.validateUser,
                    'exchange_id':self.exchangeId,
                    'participant': UserModel.find_by_id(self.participantId).username,
                    'participant_id': self.participantId
                }

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
    def find_by_exchange_id(cls, exchangeId: int) ->List:
        return cls.query.filter_by(exchangeId = exchangeId).all()

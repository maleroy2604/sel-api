from db import db
from models.user import UserModel
from models.exchangeocurence import ExchangeOcurenceModel, ExchangeOcurenceJSON
from models.message import MessageJSON
from datetime import datetime
from typing import Dict, List, Union

ExchangeJSON = Dict[str, Union[str, int, List[ExchangeOcurenceJSON], List[MessageJSON]]]


class ExchangeModel(db.Model):
    __tablename__ = 'exchanges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    currentCapacity = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    date = db.Column(db.String(80))

    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    exchangeOcurences = db.relationship('ExchangeOcurenceModel' , lazy = 'dynamic',  cascade="all, delete-orphan")
    messages = db.relationship('MessageModel' , lazy = 'dynamic',  cascade="all, delete-orphan")

    def __init__(self, name: str, description: str, date: str, capacity: int, owner: int):
        self.name = name
        self.description = description
        self.date = datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
        self.currentCapacity = 0
        self.capacity = capacity
        self.owner = owner

    def json(self) -> ExchangeJSON:
        return {
                    'id': self.id,
                    'name': self.name,
                    'description': self.description,
                    'date': self.date,
                    'capacity': self.capacity,
                    'current_capacity': self.currentCapacity,
                    'owner': self.owner,
                    'ownerName': UserModel.find_by_id(self.owner).username ,
                    'exchangeocurence': [exchangeOcurence.json() for exchangeOcurence in self.exchangeOcurences.all()],
                    'messages' : [message.json() for message in self.messages.all()]
                }

    @classmethod
    def find_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all_limit(cls, numberlimitmax: int, numberlimitmin: int) -> List:
        return cls.query.order_by(ExchangeModel.id.desc()).slice(numberlimitmin, numberlimitmax);

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def increase_current_capacity(self) -> None:
        self.currentCapacity += 1
        db.session.add(self)
        db.session.commit()

    def decrease_current_capacity(self) -> None:
        if self.currentCapacity > 0 :
            self.currentCapacity -= 1
        db.session.add(self)
        db.session.commit()

    def check_balance_owner(self, hours: int) -> None:
        user = UserModel.find_by_id(self.owner)
        return user.counterHours >= hours

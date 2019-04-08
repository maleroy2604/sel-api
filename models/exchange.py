from db import db
from models.user import UserModel
from models.exchangeocurence import ExchangeOcurenceModel
from datetime import datetime
from typing import List


class ExchangeModel(db.Model):
    __tablename__ = "exchanges"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    currentCapacity = db.Column(db.Integer, nullable=False, default=0)
    capacity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(80), nullable=False)
    ownerName = db.Column(db.String(80))

    owner = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    exchangeOcurences = db.relationship(
        "ExchangeOcurenceModel", lazy="dynamic", cascade="all, delete-orphan"
    )
    messages = db.relationship(
        "MessageModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    @classmethod
    def find_by_id(cls, id: int) -> "ExchangeModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all_limit(cls, numberlimit) -> List:
        return cls.query.order_by(ExchangeModel.id.desc()).slice(
            numberlimit.numberlimitmin, numberlimit.numberlimitmax
        )

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
        if self.currentCapacity > 0:
            self.currentCapacity -= 1
        db.session.add(self)
        db.session.commit()

    def check_balance_owner(self, hours: int) -> None:
        user = UserModel.find_by_id(self.owner)
        return user.counterHours >= hours

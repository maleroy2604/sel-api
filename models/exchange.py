from db import db
from models.user import UserModel
from models.exchangeocurence import ExchangeOcurenceModel
from typing import List
from datetime import datetime


class ExchangeModel(db.Model):
    __tablename__ = "exchanges"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    currentCapacity = db.Column(db.Integer, nullable=False, default=0)
    capacity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(80), nullable=False)
    ownerName = db.Column(db.String(80))
    avatarUrl = db.Column(db.String(80))
    category = db.Column(db.String(80))

    owner = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    exchangeOcurences = db.relationship(
        "ExchangeOcurenceModel", lazy="dynamic", cascade="all, delete-orphan"
    )
    messages = db.relationship(
        "MessageModel", lazy="dynamic", cascade="all, delete-orphan"
    )

    @classmethod
    def find_by_id(cls, _id: int) -> "ExchangeModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all_limit(cls, numberlimit) -> List:
        datetime_now = datetime.now()
        return (
            cls.query.order_by(ExchangeModel.id.desc())
            .filter(
                ExchangeModel.date
                > datetime.strftime(datetime_now, "%Y-%m-%d %H:%M:%S")
            )
            .slice(numberlimit.numberlimitmin, numberlimit.numberlimitmax)
        )

    @classmethod
    def find_all_exchange_by_id(cls, user_id) -> List:
        return cls.query.filter_by(owner=user_id)

    @classmethod
    def change_avatar_url_exchanges(cls, user_id: int, avatarurl: str) -> None:
        for exchange in ExchangeModel.find_all_exchange_by_id(user_id):
            exchange.avatarUrl = avatarurl
            exchange.save_to_db()

    @classmethod
    def change_ownername_exchange(cls, user_id: int, username: str) -> None:
        for exchange in ExchangeModel.find_all_exchange_by_id(user_id):
            exchange.ownerName = username
            exchange.save_to_db()

    @classmethod
    def change_category_exchange(cls, categoryname: str, nocategorystr: str) -> None:
        for exchange in ExchangeModel.find_all_exchange_by_category(categoryname):
            exchange.category = nocategorystr
            exchange.save_to_db()

    @classmethod
    def find_all_exchange_by_category(cls, categoryname: str) -> List:
        return cls.query.filter_by(category=categoryname)

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

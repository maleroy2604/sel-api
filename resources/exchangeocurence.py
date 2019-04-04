import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.exchangeocurence import ExchangeOcurenceModel
from models.exchange import ExchangeModel
from models.user import UserModel
from datetime import datetime

BLANK_ERROR = "'{}' can't let be blank."
NO_PLACE_AVAILABLE = "There is no place available."
ERROR_INSERTING = "An error occurred while inserting the'{}'."
NOT_ENOUGH_HOURS = "not enough hours."
NOT_FOUND_ERROR = "'{}' not found."


class ExchangeOcurence(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        "exchange_id", type=int, required=True, help=BLANK_ERROR.format("exchange_id")
    )
    parser.add_argument(
        "participant_id",
        type=int,
        required=True,
        help=BLANK_ERROR.format("participant_id"),
    )
    parser.add_argument("hours", type=int, required=False)

    @classmethod
    @jwt_required
    def post(cls, id: int):
        data = ExchangeOcurence.parser.parse_args()
        exchange = ExchangeModel.find_by_id(data["exchange_id"])
        exchangeocurence = ExchangeOcurenceModel(
            data["exchange_id"], data["participant_id"]
        )
        try:
            if exchange.currentCapacity < exchange.capacity:
                exchangeocurence.save_to_db()
                exchange.increase_current_capacity()
                return exchangeocurence.json(), 201
            else:
                return {"message": NO_PLACE_AVAILABLE}, 500
        except:
            return {"message": ERROR_INSERTING.format("exchangeocurence")}, 500

    @classmethod
    @jwt_required
    def put(cls, id: int):
        data = ExchangeOcurence.parser.parse_args()
        exchangeocurence = ExchangeOcurenceModel.find_by_id(id)
        exchange = ExchangeModel.find_by_id(data["exchange_id"])
        if exchangeocurence:
            if exchange.check_balance_owner(data["hours"]):
                user = UserModel.find_by_id(data["participant_id"])
                user.increase_counter_hours(data["hours"])
                owner = UserModel.find_by_id(exchange.owner)
                owner.decrease_counter_hours(data["hours"])
            else:
                return {"message": NOT_ENOUGH_HOURS}

            exchangeocurence.delete_from_db()
        exchange.decrease_current_capacity()

        return exchangeocurence.json(), 201
        return {"message": NOT_FOUND_ERROR.format("exchangeocurence")}, 404

    @classmethod
    @jwt_required
    def delete(cls, id: int):
        exchangeocurence = ExchangeOcurenceModel.find_by_id(id)
        exchange = ExchangeModel.find_by_id(exchangeocurence.exchangeId)
        if exchangeocurence:
            exchangeocurence.delete_from_db()
            exchange.decrease_current_capacity()
            return exchangeocurence.json(), 201
        return {"message": NOT_FOUND_ERROR.format("exchangeocurence")}, 404


class ExchangeOcurenceList(Resource):
    @classmethod
    @jwt_required
    def get(cls, exchangeId: int):
        return [
            exchangeocurence.json()
            for exchangeocurence in ExchangeOcurenceModel.find_by_exchange_id(
                exchangeId
            )
        ]

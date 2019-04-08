import sqlite3
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models.exchangeocurence import ExchangeOcurenceModel
from models.exchange import ExchangeModel
from models.user import UserModel
from datetime import datetime
from schemas.exchangeocurence import ExchangeOcurenceSchema

BLANK_ERROR = "'{}' can't let be blank."
NO_PLACE_AVAILABLE = "There is no place available."
ERROR_INSERTING = "An error occurred while inserting the'{}'."
NOT_ENOUGH_HOURS = "not enough hours."
NOT_FOUND_ERROR = "'{}' not found."

exchangeocurence_schema = ExchangeOcurenceSchema()
exchangeocurence_list_schema = ExchangeOcurenceSchema(many=True)


class ExchangeOcurence(Resource):
    @classmethod
    @jwt_required
    def post(cls, id: int):
        exchangeocurence = exchangeocurence_schema.load(request.get_json())
        exchange = ExchangeModel.find_by_id(exchangeocurence.exchangeId)
        try:
            if exchange.currentCapacity < exchange.capacity:
                exchangeocurence.save_to_db()
                exchange.increase_current_capacity()
                return exchangeocurence_schema.dump(exchangeocurence), 201
            else:
                return {"message": NO_PLACE_AVAILABLE}, 500
        except:
            return {"message": ERROR_INSERTING.format("exchangeocurence")}, 500

    @classmethod
    @jwt_required
    def put(cls, id: int):
        exchangeocurence_data = exchangeocurence_schema.load(
            request.get_json(), instance=ExchangeOcurenceModel()
        )
        exchangeocurence = ExchangeOcurenceModel.find_by_id(id)
        exchange = ExchangeModel.find_by_id(exchangeocurence_data.exchangeId)
        if exchangeocurence:
            if exchange.check_balance_owner(exchangeocurence_data.hours):
                user = UserModel.find_by_id(exchangeocurence_data.participantId)
                user.increase_counter_hours(exchangeocurence_data.hours)
                owner = UserModel.find_by_id(exchange.owner)
                owner.decrease_counter_hours(exchangeocurence_data.hours)
            else:
                return {"message": NOT_ENOUGH_HOURS}

            exchangeocurence.delete_from_db()
        exchange.decrease_current_capacity()

        return exchangeocurence_schema.dump(exchangeocurence), 201
        return {"message": NOT_FOUND_ERROR.format("exchangeocurence")}, 404

    @classmethod
    @jwt_required
    def delete(cls, id: int):
        exchangeocurence = ExchangeOcurenceModel.find_by_id(id)
        exchange = ExchangeModel.find_by_id(exchangeocurence.exchangeId)
        if exchangeocurence:
            exchangeocurence.delete_from_db()
            exchange.decrease_current_capacity()
            return exchangeocurence_schema.dump(exchangeocurence), 201
        return {"message": NOT_FOUND_ERROR.format("exchangeocurence")}, 404


class ExchangeOcurenceList(Resource):
    @classmethod
    @jwt_required
    def get(cls, exchangeId: int):
        return exchangeocurence_list_schema.dump(
            ExchangeOcurenceModel.find_by_exchange_id(exchangeId)
        )

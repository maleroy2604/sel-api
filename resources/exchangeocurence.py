import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.exchangeocurence import ExchangeOcurenceModel
from models.exchange import ExchangeModel
from models.user import UserModel
from datetime import datetime

class ExchangeOcurence(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('validateuser',
        type = int
    )
    parser.add_argument('exchange_id',
        type = int,
        required = True,
        help ="exchangeid is required"
    )
    parser.add_argument('participant_id',
        type = int,
        required = True,
        help = "participant_id is required"
    )
    parser.add_argument('hours',
        type = int
    )

    @jwt_required()
    def post(self, id):
        data = ExchangeOcurence.parser.parse_args()
        exchange = ExchangeModel.find_by_id(data['exchange_id'])
        exchangeocurence = ExchangeOcurenceModel(data['exchange_id'], data['participant_id'])
        try:
            if exchange.currentCapacity < exchange.capacity :
                exchangeocurence.save_to_db()
                exchange.increase_current_capacity()
                return exchangeocurence.json(), 201
            else :
                return {'message':"There is no place available"}
        except:
            return {'message':"An error occured inserting the exchangeocurence"}, 500

    @jwt_required()
    def put(self, id):
        data = ExchangeOcurence.parser.parse_args()
        exchangeocurence = ExchangeOcurenceModel.find_by_id(id)
        exchange = ExchangeModel.find_by_id(data['exchange_id'])
        if exchangeocurence:
            if exchange.check_balance_owner(data['hours']):
                user = UserModel.find_by_id(data['participant_id'])
                user.increase_counter_hours(data['hours'])
                owner = UserModel.find_by_id(exchange.owner)
                owner.decrease_counter_hours(data['hours'])
            else:
                return {'message':"Not enough hours"}

            exchangeocurence.delete_from_db()
        exchange.decrease_current_capacity()

        return exchangeocurence.json() , 201
        return {'message': "Exchangeocurence not found"}, 404

    @jwt_required()
    def delete(self, id):
        exchangeocurence = ExchangeOcurenceModel.find_by_id(id)
        exchange = ExchangeModel.find_by_id(exchangeocurence.exchangeId)
        if exchangeocurence:
            exchangeocurence.delete_from_db()
            exchange.decrease_current_capacity()
            return exchangeocurence.json(), 201
        return {'message': "Exchangeocurence not found"}, 404


class ExchangeOcurenceList(Resource):
    @jwt_required()
    def get(self, exchangeId):
        return [exchangeocurence.json() for exchangeocurence in ExchangeOcurenceModel.find_by_exchange_id(exchangeId)]

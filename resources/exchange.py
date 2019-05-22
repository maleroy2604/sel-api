from flask_restful import Resource
from flask import request
from schemas.exchange import ExchangeSchema
from schemas.numberlimit import NumberLimitSchema
from flask_jwt_extended import jwt_required
from models.exchange import ExchangeModel
from libs.strings import gettext
from libs.decorator import verify_permission

exchange_schema = ExchangeSchema()
exchange_list_schema = ExchangeSchema(many=True)
numberlimit_schema = NumberLimitSchema()


class Exchange(Resource):
    @classmethod
    @jwt_required
    def get(cls, id: int):
        exchange = ExchangeModel.find_by_id(id)
        if exchange:
            return exchange_schema.dump(exchange)
        return {"message": gettext("not_found_error").format("exchange")}, 404

    @classmethod
    @jwt_required
    def post(cls, id: int):
        exchange = exchange_schema.load(request.get_json())
        try:
            exchange.save_to_db()
        except:
            return {"message": gettext("error_inserting").format("exchange")}, 500
        return exchange_schema.dump(exchange), 201

    @classmethod
    @jwt_required
    # @verify_permission
    def delete(cls, id: int):
        exchange = ExchangeModel.find_by_id(id)
        if exchange:
            exchange.delete_from_db()
            return exchange_schema.dump(exchange)
        return {"message": gettext("not_found_error").format("message")}, 404

    @jwt_required
    def put(self, id: int):
        exchange_data = exchange_schema.load(
            request.get_json(), instance=ExchangeModel()
        )
        exchange = ExchangeModel.find_by_id(id)
        if exchange:
            exchange.name = exchange_data.name
            exchange.description = exchange_data.description
            exchange.currentCapacity = exchange_data.currentCapacity
            exchange.capacity = exchange_data.capacity
            exchange.date = exchange_data.date
            exchange.category = exchange_data.category
            try:
                exchange.save_to_db()
            except:
                return {"message": gettext("error_inserting").format("exchange")}, 500
            return exchange_schema.dump(exchange), 201
        return {"message": gettext("not_found_error").format("message")}, 404


class ExchangeList(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        numberlimit = numberlimit_schema.load(request.get_json())
        return exchange_list_schema.dump(ExchangeModel.find_all_limit(numberlimit))

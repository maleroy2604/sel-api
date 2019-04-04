from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.exchange import ExchangeModel

BLANK_ERROR = "'{}' can't let be blank."
NOT_FOUND_ERROR = "'{}' not found."
ERROR_INSERTING = "An error occurred while inserting the'{}'."


class Exchange(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help=BLANK_ERROR.format("name")
    )
    parser.add_argument(
        "description", type=str, required=True, help=BLANK_ERROR.format("description")
    )
    parser.add_argument(
        "date", type=str, required=True, help=BLANK_ERROR.format("date")
    )
    parser.add_argument(
        "capacity",
        type=int,
        default=1,
        required=True,
        help=BLANK_ERROR.format("capacity"),
    )
    parser.add_argument(
        "owner", type=int, required=True, help=BLANK_ERROR.format("owner")
    )

    @classmethod
    @jwt_required
    def get(cls, id: int):
        exchange = ExchangeModel.find_by_id(id)
        if exchange:
            return exchange.json()
        return {"message": NOT_FOUND_ERROR.format("exchange")}, 404

    @classmethod
    @jwt_required
    def post(cls, id: int):
        data = Exchange.parser.parse_args()
        exchange = ExchangeModel(**data)
        try:
            exchange.save_to_db()
        except:
            return {"message": ERROR_INSERTING.format("exchange")}, 500
        return exchange.json(), 201

    @classmethod
    @jwt_required
    def delete(cls, id: int):
        exchange = ExchangeModel.find_by_id(id)
        if exchange:
            exchange.delete_from_db()
            return exchange.json()
        return {"message": NOT_FOUND_ERROR.format("message")}, 404

    @jwt_required
    def put(self, id: int):
        data = Exchange.parser.parse_args()
        exchange = ExchangeModel.find_by_id(id)
        if exchange:
            exchange.name = data["name"]
            exchange.date = data["date"]
            exchange.description = data["description"]
            exchange.capacity = data["capacity"]
            try:
                exchange.save_to_db()
            except:
                return {"message": ERROR_INSERTING.format("exchange")}, 500
            return exchange.json(), 201
        return {"message": NOT_FOUND_ERROR.format("message")}, 404


class ExchangeList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "numberlimitmax",
        type=int,
        required=True,
        help=BLANK_ERROR.format("numberlimitmax"),
    )
    parser.add_argument(
        "numberlimitmin",
        type=int,
        required=True,
        help=BLANK_ERROR.format("numberlimitmin"),
    )

    @classmethod
    @jwt_required
    def post(cls):
        data = ExchangeList.parser.parse_args()
        return [exchange.json() for exchange in ExchangeModel.find_all_limit(**data)]

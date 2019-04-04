from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.exchange import ExchangeModel

class Exchange(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type = str,
        required = True,
        help = "name is required"
    )
    parser.add_argument('description',
        type = str,
        required = True,
        help = "description is required"
    )
    parser.add_argument('date',
        type = str,
        required = True,
        help = "date is required"
    )
    parser.add_argument('capacity',
        type = int,
        default = 1,
        required = True,
        help = "capacity is required"
    )
    parser.add_argument('owner',
        type = int,
        required = True,
        help = "owner is required"
    )

    @jwt_required
    def get(self, id: int):
        exchange = ExchangeModel.find_by_id(id)
        if exchange:
            return exchange.json()
        return {'message': 'exchange not found'}, 404

    @jwt_required
    def post(self, id: int):
        data = Exchange.parser.parse_args()
        exchange = ExchangeModel(**data)
        try:
            exchange.save_to_db()
        except:
            return {'message':"An error occured inserting the exchange"},500
        return exchange.json(), 201

    @jwt_required
    def delete(self, id: int):
        exchange = ExchangeModel.find_by_id(id)
        if exchange:
            exchange.delete_from_db()
            return exchange.json()
        return {'message': "Exchange not found"}, 404

    @jwt_required
    def put(self, id: int):
        data = Exchange.parser.parse_args()
        exchange = ExchangeModel.find_by_id(id)
        if exchange:
            exchange.name = data['name']
            exchange.date = data['date']
            exchange.description = data['description']
            exchange.capacity = data['capacity']
            try:
                exchange.save_to_db()
            except:
                return {'message':"An error occured while inserting the exchange"}, 500
            return exchange.json(), 201
        return {'message': "Exchange not found"}, 404


class ExchangeList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('numberlimitmax',
        type = int,
        required = True,
        help = "max is required"
    )
    parser.add_argument('numberlimitmin',
        type = int,
        required = True,
        help = "min is required"
    )
    @jwt_required
    def post(self):
        data = ExchangeList.parser.parse_args()
        return [exchange.json() for exchange in ExchangeModel.find_all_limit(**data)]

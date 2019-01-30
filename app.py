
import datetime
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import User, UserList
from resources.exchange import Exchange, ExchangeList
from resources.exchangeocurence import ExchangeOcurence, ExchangeOcurenceList
from resources.message import Message

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=7200)
app.secret_key = 'martin'
api = Api(app)

jwt = JWT(app, authenticate, identity)
api.add_resource(User, '/user/<string:username>')
api.add_resource(UserList, '/users')
api.add_resource(Exchange, '/exchange/<int:id>')
api.add_resource(ExchangeList, '/exchanges')
api.add_resource(ExchangeOcurence, '/exchangeocurence/<int:id>')
api.add_resource(ExchangeOcurenceList, '/exchangeocurences/<exchangeId>')
api.add_resource(Message, '/message/<int:id>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000, debug=True)

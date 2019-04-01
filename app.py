import os
import datetime
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import User, UserList
from resources.userregister import UserRegister
from resources.tokenrefresh import TokenRefresh
from resources.exchange import Exchange, ExchangeList
from resources.exchangeocurence import ExchangeOcurence, ExchangeOcurenceList
from resources.message import Message
from resources.authenticate import Authenticate

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=7200000)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'martin'
api = Api(app)

jwt = JWTManager(app)

api.add_resource(User, '/user/<int:id>')
api.add_resource(UserList, '/users')
api.add_resource(UserRegister, '/register')
api.add_resource(TokenRefresh, '/tokenrefresh')
api.add_resource(Exchange, '/exchange/<int:id>')
api.add_resource(ExchangeList, '/exchanges/<int:numberlimit>')
api.add_resource(ExchangeOcurence, '/exchangeocurence/<int:id>')
api.add_resource(ExchangeOcurenceList, '/exchangeocurences/<exchangeId>')
api.add_resource(Message, '/message/<int:id>')
api.add_resource(Authenticate, '/authenticate')


if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)

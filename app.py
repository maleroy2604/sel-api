from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from resources.user import User, UserList
from resources.userregister import UserRegister
from resources.tokenrefresh import TokenRefresh
from resources.exchange import Exchange, ExchangeList
from resources.exchangeocurence import ExchangeOcurence, ExchangeOcurenceList
from resources.message import Message
from resources.authenticate import Authenticate
from resources.userlogout import UserLogout
from blacklist import BLACKLIST
from ma import ma

app = Flask(__name__)
app.secret_key = "martin"
app.config.from_object("config")
api = Api(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(User, "/user/<int:id>")
api.add_resource(UserList, "/users")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogout, "/userlogout")

api.add_resource(TokenRefresh, "/tokenrefresh")
api.add_resource(Authenticate, "/authenticate")

api.add_resource(Exchange, "/exchange/<int:id>")
api.add_resource(ExchangeList, "/exchanges")
api.add_resource(ExchangeOcurence, "/exchangeocurence/<int:id>")
api.add_resource(ExchangeOcurenceList, "/exchangeocurences/<exchangeId>")

api.add_resource(Message, "/message/<int:id>")


if __name__ == "__main__":
    from db import db

    db.init_app(app)
    ma.init_app(app)

    if app.config["DEBUG"]:

        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)

from ma import ma
from models.user import UserModel
from schemas.exchange import ExchangeSchema
from schemas.exchangeocurence import ExchangeOcurenceSchema
from schemas.category import CategorySchema


class UserSchema(ma.ModelSchema):
    exchanges = ma.Nested(ExchangeSchema, many=True)
    exchangeocurences = ma.Nested(ExchangeOcurenceSchema, many=True)
    category = ma.Nested(CategorySchema, many=True)

    class Meta:
        model = UserModel
        load_only = ("password", "confirmpassword")

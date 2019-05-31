from ma import ma
from models.exchange import ExchangeModel
from models.exchangeocurence import ExchangeOcurenceModel
from schemas.exchangeocurence import ExchangeOcurenceSchema
from schemas.message import MessageSchema


class ExchangeSchema(ma.ModelSchema):
    exchangeOcurences = ma.Nested(ExchangeOcurenceSchema, many=True)
    messages = ma.Nested(MessageSchema, many=True)

    class Meta:
        model = ExchangeModel
        load_only = ("user",)
        include_fk = True

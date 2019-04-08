from ma import ma
from models.exchange import ExchangeModel
from models.exchangeocurence import ExchangeOcurenceModel
from schemas.exchangeocurence import ExchangeOcurenceSchema


class ExchangeSchema(ma.ModelSchema):
    exchangeOcurences = ma.Nested(ExchangeOcurenceSchema, many=True)

    class Meta:
        model = ExchangeModel
        load_only = ("user",)
        include_fk = True

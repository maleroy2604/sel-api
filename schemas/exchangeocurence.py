from ma import ma
from models.exchange import ExchangeOcurenceModel


class ExchangeOcurenceSchema(ma.ModelSchema):
    class Meta:
        model = ExchangeOcurenceModel
        load_only = ("exchange", "participant")
        include_fk = True

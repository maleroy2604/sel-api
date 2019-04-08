from ma import ma
from models.numberlimit import NumberLimit


class NumberLimitSchema(ma.ModelSchema):
    class Meta:
        model = NumberLimit

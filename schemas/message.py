from ma import ma
from models.message import MessageModel
from schemas.user import UserSchema

class MessageSchema(ma.ModelSchema):
    sender = ma.Nested(UserSchema)

    class Meta:
        model = MessageModel
        load_only = ("user","exchange")

from ma import ma
from models.message import MessageModel


class MessageSchema(ma.ModelSchema):
    class Meta:
        model = MessageModel
        load_only = ("exchange", "sender")
        include_fk = True

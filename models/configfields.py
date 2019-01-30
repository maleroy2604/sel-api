from flask_restful import fields

user_fields = {
    'username': fields.String
}

messages_fields = {
    'id': fields.Integer,
    'message': fields.String,
}

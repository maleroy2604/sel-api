from db import db
from datetime import datetime
from flask_restful import marshal
#from models.configfields import messages_fields

#recipients = db.Table('recipients',
#    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#    db.Column('message_id', db.Integer, db.ForeignKey('messages.id'))
#)


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))
    counterHours = db.Column(db.Integer)

    exchanges = db.relationship('ExchangeModel', lazy = 'dynamic', cascade="all, delete-orphan")
    exchangeOcurences = db.relationship('ExchangeOcurenceModel', lazy = 'dynamic', cascade="all, delete-orphan")
    messagesSends = db.relationship('MessageModel', lazy = 'dynamic', cascade="all, delete-orphan")

    #messages_recipient = db.relationship('MessageModel', secondary = recipients, lazy = 'dynamic', backref = db.backref('users_recipient', lazy = 'dynamic') )


    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.counterHours = 2

    def json(self):
        return {
                'id': self.id,
                'username': self.username,
                #'password': self.password,
                #'email': self.email,
                'counterhours': self.counterHours,
                #'exchangeocurence': [exchangeOcurence.json() for exchangeOcurence in self.exchangeOcurences.all()],
                #'message': [marshal(message, messages_fields) for message in self.messages_recipient]
                }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def increase_counter_hours(self, hours):
        self.counterHours += hours

    def decrease_counter_hours(self, hours):
        self.counterHours -= hours

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_participants(cls, exchangeOcurences):
        users = []
        for exchangeocurence in exchangeOcurences:
            users.append(UserModel.find_by_id(exchangeocurence.participantId))
        return users

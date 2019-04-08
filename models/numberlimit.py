from db import db


class NumberLimit(db.Model):
    __tablename__ = "numberlimit"

    id = db.Column(db.Integer, primary_key=True)
    numberlimitmin = db.Column(db.Integer, nullable=False)
    numberlimitmax = db.Column(db.Integer, nullable=False)

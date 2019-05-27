from db import db
from typing import List


class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    imagename = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(256), nullable=False)

    owner = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, categoryname: str):
        return cls.query.filter_by(category=categoryname).first()

    @classmethod
    def find_by_id(cls, id: int):
        return cls.query.filter_by(owner=id).first()

    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_my_categories(cls, id: int) -> List:
        return cls.query.filter_by(owner=id)

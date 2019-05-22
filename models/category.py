from db import db
from typing import List


class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(256), nullable=False)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, categoryname: str) -> List:
        return cls.query.filter_by(category=categoryname).first()

    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()

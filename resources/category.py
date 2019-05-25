from flask_restful import Resource
from schemas.category import CategorySchema
from models.category import CategoryModel
from flask_jwt_extended import jwt_required
from flask import request
from libs.strings import gettext

category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)


class CategoryList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return category_list_schema.dump(CategoryModel.find_all())

    @classmethod
    @jwt_required
    def post(cls):
        data = category_schema.load(request.get_json())
        category = CategoryModel.find_by_name(data.category)
        if category:
            return {"message": gettext("already_exists").format("category")}, 400
        data.save_to_db()
        category_schema.dump(data), 201


class MyCategoryList(Resource):
    @classmethod
    @jwt_required
    def get(cls, id: int):
        return category_list_schema.dump(CategoryModel.find_my_categories(id))

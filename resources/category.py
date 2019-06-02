from flask_restful import Resource
from schemas.category import CategorySchema
from models.category import CategoryModel
from models.exchange import ExchangeModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from libs.strings import gettext
import os
from libs import image_helper


category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)


class CategoryList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return category_list_schema.dump(CategoryModel.find_all())

    @classmethod
    @jwt_required
    def post(cls, id: int):
        data = category_schema.load(request.get_json(), instance=CategoryModel())
        category = CategoryModel.find_by_name(data.category)
        if category:
            return {"message": gettext("already_exists").format("category")}, 400
        data.save_to_db()
        category_schema.dump(data), 201

    @classmethod
    @jwt_required
    def delete(cls, id: int):
        category = CategoryModel.find_by_id(id)
        folder = "category"
        if category:
            {"message": gettext("not_found_error").format("category")}, 500
        if category.owner != get_jwt_identity():
            {"message": gettext("not_allow")}, 500
        ExchangeModel.change_category_exchange(category.category)
        category.delete_from_db()
        return category_list_schema.dump(CategoryModel.find_my_categories(id)), 201

    @classmethod
    @jwt_required
    def put(cls):
        data = category_schema.load(request.get_json(), instance=CategoryModel())
        folder = "category"
        category = CategoryModel.find_by_id(data.owner)
        if data.owner != get_jwt_identity():
            {"message": gettext("not_allow")}, 500
        image_helper.update_name_image(folder=folder, NewName=data.filename)
        category.category = data.category
        category.save_to_db()
        return category_list_schema.dump(CategoryModel.find_my_categories(id)), 201


class MyCategoryList(Resource):
    @classmethod
    @jwt_required
    def get(cls, id: int):
        return category_list_schema.dump(CategoryModel.find_my_categories(id))

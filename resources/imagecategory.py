from flask_restful import Resource
from flask import send_file, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from flask_uploads import UploadNotAllowed
from libs import image_helper
from schemas.image import ImageSchema
from schemas.category import CategorySchema
from models.category import CategoryModel
from libs.strings import gettext

image_schema = ImageSchema()
category_schema = CategorySchema()


class UploadImageCategory(Resource):
    @jwt_required
    def post(self, id: int):
        data = image_schema.load(request.files)
        folder = "category"
        if id != get_jwt_identity():
            return {"message": gettext("not_allow")}, 500
        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            filename = image_helper.get_filename(basename)
            category = CategoryModel.find_by_name(filename)
            category.filename = filename
            category.save_to_db()
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("update_image_fail").format(extension)}, 400

    @jwt_required
    def delete(self, id: int):
        folder = "category"
        if id != get_jwt_identity():
            return {"message": gettext("not_allow")}, 500
        filename = CategoryModel.find_by_id(id).imagename
        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_illegal_name").format(filename)}, 400
        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {"message": gettext("deleted_image_success").format(filename)}, 200
        except FileNotFoundError:
            return {"message": gettext("image_not_found")}, 404
        except:
            traceback.print_exc()
            return {"message": gettext("delete_image_fail")}, 500


class ImageCategory(Resource):
    @jwt_required
    def get(self, filename: str):
        folder = "category"
        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_illegal_format".format(filename))}
        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": gettext("image_not_found")}, 404

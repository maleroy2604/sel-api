from flask_restful import Resource
from flask import send_file, request
from flask_jwt_extended import jwt_required
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
    def post(self):
        data = image_schema.load(request.files)
        folder = "category"
        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            filename = image_helper.get_filename(basename)
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("update_image_fail").format(extension)}, 400


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

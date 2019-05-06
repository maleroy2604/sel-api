from flask_restful import Resource
from flask import send_file, request
from flask_jwt_extended import jwt_required
import os
from libs import image_helper
from schemas.image import ImageSchema

image_schema = ImageSchema()


class ImageExchange(Resource):
    @jwt_required
    def get(self, filename: str):
        folder = "category"
        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_illegal_format".format(filename))}
        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": gettext("image_not_found")}, 404

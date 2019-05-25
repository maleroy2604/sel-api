from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import send_file, request
from models.user import UserModel
from models.exchange import ExchangeModel
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import os

from libs.strings import gettext
from libs import image_helper
from schemas.image import ImageSchema
from schemas.user import UserSchema


image_schema = ImageSchema()
user_schema = UserSchema()

UPDATE_IMAGE_SUCCESS = "Image {} uploaded with success"
UPDATE_IMAGE_FAIL = "Extension {} is not autorise"


class ImageUploadAvatar(Resource):
    @jwt_required
    def post(self, id: int):
        folder = "imageavatar"
        data = image_schema.load(request.files)
        if id != get_jwt_identity():
            return {"message": gettext("not_allow")}, 500
        user = UserModel.find_by_id(id)
        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            user.imagename = basename
            user.save_to_db()
            ExchangeModel.change_avatar_url_exchanges(id, user.imagename)
            return user_schema.dump(user), 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("update_image_fail").format(extension)}, 400

    @jwt_required
    def delete(self, id: int):
        folder = "imageavatar"
        if id != get_jwt_identity():
            return {"message": gettext("not_allow")}, 500
        filename = UserModel.find_by_id(id).imagename
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


class ImageAvatar(Resource):
    @jwt_required
    def get(self, filename: str):
        folder = "imageavatar"
        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_illegal_format".format(filename))}
        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": gettext("image_not_found")}, 404

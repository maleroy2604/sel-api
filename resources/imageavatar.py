from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import send_file, request
from models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import os

from libs.strings import gettext
from libs import image_helper
from schemas.image import ImageSchema


image_schema = ImageSchema()

UPDATE_IMAGE_SUCCESS = "Image {} uploaded with success"
UPDATE_IMAGE_FAIL = "Extension {} is not autorise"


class ImageUploadAvatar(Resource):
    @jwt_required
    def post(self):
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        user = UserModel.find_by_id(user_id)
        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            # if user.avatarurl is not None:
            #    index = user.avatarurl.rfind("/")
            #    sub_string = user.avatarurl[index + 1 : index + len(user.avatarurl)]
            #    os.remove(image_helper.get_path(sub_string, folder=folder))
            user.avatarurl = "https://sel-app.herokuapp.com/imageavatar/" + basename
            # user.avatarurl = "http://10.0.2.2:5000/imageavatar/" + basename
            user.save_to_db()
            return {"message": gettext("update_image_success").format(image_path)}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("update_image_fail").format(extension)}, 400


class ImageAvatar(Resource):
    @jwt_required
    def get(self, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_illegal_format".format(filename))}
        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": gettext("image_not_found")}, 404

    @jwt_required
    def delete(self, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

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

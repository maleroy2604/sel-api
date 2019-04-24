from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity


from libs import image_helper
from schemas.image import ImageSchema

image_schema = ImageSchema()

UPDATE_IMAGE_SUCCESS = "Image {} uploaded with success"
UPDATE_IMAGE_FAIL = "Extension {} is not autorise"


class ImageUpload(Resource):
    @jwt_required
    def post(self):
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            return {"message": UPDATE_IMAGE_SUCCESS.format(image_path)}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": UPDATE_IMAGE_FAIL.format(extension)}, 400

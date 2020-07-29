import io
from io import BytesIO

from PIL import Image, UnidentifiedImageError
from dropbox import dropbox
from dropbox.exceptions import AuthError, ApiError, BadInputError
from dropbox.stone_validators import ValidationError
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename

from sheet.auth import jwt_required

bp = Blueprint("image", __name__, url_prefix="/image")


@bp.route('/convert', methods=['POST'])
@jwt_required
def convert():
    """Converts a file image to jpeg or png."""
    if 'file' not in request.files:
        return jsonify(message='No file was sent.'), 400

    if 'format' not in request.form:
        return jsonify(message='Missing format parameter.'), 400

    img_format = request.form.get('format')

    file = request.files['file']
    img_name = secure_filename(file.filename)
    img_io, code = convert_image(file, img_format)

    if code != 200:
        return img_io, code

    return send_file(img_io, mimetype=f'image/{img_format}', attachment_filename=img_name, as_attachment=True)


@bp.route('/convert/fromdropbox', methods=['POST'])
@jwt_required
def convert_fromdropbox(access_token=None):
    """Converts a Dropbox file image to jpeg or png."""
    if not access_token:
        return jsonify(message='Missing access_token parameter.'), 400

    if 'path' not in request.form:
        return jsonify(message='Missing path parameter.'), 400

    if 'format' not in request.form:
        return jsonify(message='Missing format parameter.'), 400

    dbx = dropbox.Dropbox(access_token)

    try:
        dbx.users_get_current_account()
    except (AuthError, BadInputError):
        return jsonify(message="Invalid Dropbox access token."), 401

    path = request.form.get('path')
    img_format = request.form.get('format')

    try:
        metadata, response = dbx.files_download(path)
    except ValidationError:
        return jsonify(message="Invalid Dropbox path."), 400
    except ApiError:
        return jsonify(message="Dropbox file not found."), 404

    img_name = secure_filename(metadata.name)
    img_io, code = convert_image(io.BytesIO(response.content), img_format)

    if code != 200:
        return img_io, code

    return send_file(img_io, mimetype=f'image/{img_format}', attachment_filename=img_name, as_attachment=True)


def convert_image(image, img_format):
    """Converts image to jpeg or png."""
    allowed_conversion_formats = ['jpeg', 'png']

    if img_format not in allowed_conversion_formats:
        message = 'Format not allowed. Allowed conversion formats: {}.'.format(', '.join(allowed_conversion_formats))
        return jsonify(message=message), 400

    try:
        img = Image.open(image).convert('RGBA')

        if img_format == 'jpeg':
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, img)
            img = bg.copy()
            bg.close()

        img_io = BytesIO()
        img.save(img_io, img_format)
        img_io.seek(0)
    except UnidentifiedImageError:
        return jsonify(message='The file is not an image.'), 400

    return img_io, 200

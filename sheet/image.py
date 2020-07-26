from io import BytesIO

from PIL import Image
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename

from sheet.auth import jwt_required

bp = Blueprint("image", __name__, url_prefix="/image")


@bp.route('/convert', methods=['POST'])
@jwt_required
def convert():
    allowed_conversion_formats = ['jpeg', 'png']

    if 'file' not in request.files:
        return jsonify(message='No file was sent'), 400

    if 'format' not in request.form:
        return jsonify(message='You need to specify the format: {}.'.format(', '.join(allowed_conversion_formats))), 400

    img_format = request.form.get('format')

    if img_format not in allowed_conversion_formats:
        message = 'Format not allowed. Allowed conversion formats: {}.'.format(', '.join(allowed_conversion_formats))
        return jsonify(message=message), 400

    file = request.files['file']

    im = Image.open(file).convert("RGBA")

    if img_format == 'jpeg':
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, im)
        im = bg.copy()
        bg.close()

    img_name = secure_filename(file.filename)
    img_io = BytesIO()
    im.save(img_io, img_format)
    img_io.seek(0)

    return send_file(img_io, mimetype=f'image/{img_format}', attachment_filename=img_name, as_attachment=True)

from functools import wraps

import jwt
from flask import request, jsonify

from sheet import app


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            authorization = request.headers.get('Authorization')

            if not authorization:
                return jsonify(message='Missing Authorization headers.'), 400

            scheme, token = authorization.split(None, 1)

            if scheme != 'Bearer':
                return jsonify(message='Invalid Authorization headers.'), 400

            data = jwt.decode(token, app.config.get('SECRET_KEY'))
            email = data.get('email')

            if not email:
                return jsonify(message='Missing email parameter.'), 400

            if email not in app.config.get('AUTHORIZED_USERS', []):
                return jsonify(message='Email not authorized.'), 401
        except jwt.InvalidSignatureError:
            return jsonify(message='Invalid signature.'), 401
        except jwt.ExpiredSignatureError:
            return jsonify(message='Expired signature.'), 401
        except jwt.InvalidTokenError:
            return jsonify(message='Invalid token.'), 401

        return f(*args, **kwargs)

    return decorated

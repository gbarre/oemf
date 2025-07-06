from flask import current_app, request
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from werkzeug.security import check_password_hash
import jwt
import time

from models.user import User
from utils import Utils


def generate_token():
    # Load user
    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        raise BadRequest()

    # Ensure user exiss in database
    user = User.query.filter_by(email=data['email']).one_or_none()
    if user is None:
        msg = f'The requested user `{data["email"]}` has not been found.'
        raise NotFound(description=msg)

    # Ensure password is correct
    if not check_password_hash(user.encrypted_password, data['password']):
        raise Unauthorized(description='Wrong password!')

    timestamp = _current_timestamp()
    payload = {
        "iss": current_app.config['JWT']['issuer'],
        "iat": int(timestamp),
        "exp": int(timestamp + current_app.config['JWT']['lifetime']),
        "sub": str(data['email']),
        "userid": user.id,
    }

    return {
        'jwt': jwt.encode(
            payload,
            current_app.config['JWT']['secret'],
            algorithm=current_app.config['JWT']['algorithm'],
        ),
    }


def _current_timestamp() -> int:
    return int(time.time())


def pass_options():
    return request.headers


@Utils.require_auth
def refresh_token():
    timestamp = _current_timestamp()
    payload = {
        "iss": current_app.config['JWT']['issuer'],
        "iat": int(timestamp),
        "exp": int(timestamp + current_app.config['JWT']['lifetime']),
        "sub": str(request.decoded_token['sub']),
    }

    return {
        'jwt': jwt.encode(
            payload,
            current_app.config['JWT']['secret'],
            algorithm=current_app.config['JWT']['algorithm'],
        ),
    }

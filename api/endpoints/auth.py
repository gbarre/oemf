"""Authentication endpoints for the API."""

# Copyright (c) 2025 oemf.jrmv.net

import time

import jwt
from flask import current_app, request
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from werkzeug.security import check_password_hash

from models.user import User
from utils import Utils


def generate_token() -> dict:
    """Generate a JWT token for the user based on email and password.

    Raises:
        BadRequest: If the request does not contain the required fields.
        NotFound: If the user with the provided email does not exist.
        Unauthorized: If the password is incorrect.

    Returns:
        dict: A dictionary containing the JWT token.

    """
    # Load user
    data = request.get_json()
    if "email" not in data or "password" not in data:
        raise BadRequest

    # Ensure user exiss in database
    user = User.query.filter_by(email=data["email"]).one_or_none()
    if user is None:
        msg = f'The requested user `{data["email"]}` has not been found.'
        raise NotFound(description=msg)

    # Ensure password is correct
    if not check_password_hash(user.encrypted_password, data["password"]):
        raise Unauthorized(description="Wrong password!")

    timestamp = _current_timestamp()
    payload = {
        "iss": current_app.config["JWT"]["issuer"],
        "iat": int(timestamp),
        "exp": int(timestamp + current_app.config["JWT"]["lifetime"]),
        "sub": str(data["email"]),
        "userid": user.id,
    }

    return {
        "jwt": jwt.encode(
            payload,
            current_app.config["JWT"]["secret"],
            algorithm=current_app.config["JWT"]["algorithm"],
        ),
    }


def _current_timestamp() -> int:
    """Get the current timestamp in seconds.

    Returns:
        int: The current timestamp in seconds since the epoch.

    """
    return int(time.time())


def pass_options() -> dict:
    """Handle OPTIONS requests for CORS preflight.

    Returns:
        dict: A dictionary containing the headers for the request.

    """
    return request.headers


@Utils.require_auth
def refresh_token() -> dict:
    """Refresh the JWT token for the current user.

    Returns:
        dict: A dictionary containing the new JWT token.

    """
    timestamp = _current_timestamp()
    payload = {
        "iss": current_app.config["JWT"]["issuer"],
        "iat": int(timestamp),
        "exp": int(timestamp + current_app.config["JWT"]["lifetime"]),
        "sub": str(request.decoded_token["sub"]),
    }

    return {
        "jwt": jwt.encode(
            payload,
            current_app.config["JWT"]["secret"],
            algorithm=current_app.config["JWT"]["algorithm"],
        ),
    }


@Utils.require_auth
def is_admin() -> dict:
    """Check if the current user is an admin.

    Returns:
        dict: A dictionary indicating whether the user is an admin.

    """
    return {"admin": Utils.is_admin()}

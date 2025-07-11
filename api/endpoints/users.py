"""User management endpoints for the API."""

# Copyright (c) 2025 oemf.jrmv.net

from typing import Optional

from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, Forbidden
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from models.user import User, user_put_schema, user_schema, users_schema
from utils import Utils


@Utils.require_admin_token
def search(offset: int, limit: int, filters: Optional(dict) = None) -> list:
    """Search for user profiles with optional filters.

    Raises:
        BadRequest: If the provided filters are invalid or if there is an issue
        with the database query.

    Returns:
        A list of user profiles matching the search criteria.

    """
    try:
        query = Utils.build_query_filters(User, filters)
        users = User.query.filter(*query)\
            .limit(limit).offset(offset).all()
    except AttributeError as e:
        msg = f"Something with filters `{filters}` is wrong..."
        raise BadRequest(description=msg) from e

    if not users:  # pragma: no cover
        return [], 200
    return users_schema.dump(users)


def post(user_data: object = None) -> tuple:
    """Create a new user profile.

    Raises:
        BadRequest: If the provided data is invalid.
        Conflict: If a user with the same email already exists in the database.

    Returns:
        tuple: A tuple containing the created user profile and the HTTP status
        code 201, along with a Location header pointing to the user profile
        URL.

    """
    if user_data is None:
        user_data = request.get_json()
    try:
        data = user_schema.load(user_data)
    except ValidationError as err:
        raise BadRequest(description=str(err)) from err
    hashed_password = generate_password_hash(data["password"])
    data["encrypted_password"] = hashed_password
    data.pop("password", None)
    user = User(**data)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as e:
        msg = "A user already exists in database with the same email."
        raise Conflict(description=msg) from e

    return user_schema.dump(user), 201, {
        "Location": f"{request.base_url}/users/{user.id}",
    }


@Utils.require_auth
def get(user_id: int) -> tuple:
    """Get a user profile.

    Raises:
        Forbidden: If the user is not an admin or trying to get another user's
        profile.

    Returns:
        tuple: A tuple containing the user profile and the HTTP status code
        200, along with a Location header pointing to the user profile URL.

    """
    user_in_db = Utils.get_from_db(User, user_id)
    if not Utils.is_admin() and user_in_db.id != Utils.get_userid():
        raise Forbidden(description="You can only get your own profile.")
    user = user_schema.dump(user_in_db)
    return user, 200, {
        "Location": f"{request.base_url}/users/{user_in_db.id}",
    }


@Utils.require_auth
def put(user_id: int, **kwargs: object) -> tuple:
    """Update a user profile.

    Raises:
        Forbidden: If the user is not an admin or trying to edit another user's
        profile.
        Conflict: If a user with the same email already exists in the
        database.
        BadRequest: If the provided data is invalid or if the current
        password is incorrect when changing the password.

    Returns:
        tuple: A tuple containing the updated user profile and the HTTP status
        code 200, along with a Location header pointing to the updated user
        profile URL.

    """
    user_in_db = Utils.get_from_db(User, user_id)
    if not Utils.is_admin() and user_in_db.id != Utils.get_userid():
        raise Forbidden(description="You can only edit your own profile.")
    user_data = kwargs.get("body", {})
    try:
        data = user_put_schema.load(user_data)
    except ValidationError as err:
        raise BadRequest(description=str(err)) from err
    if not Utils.is_admin() and \
       "email" in data and \
       data["email"] != user_in_db.email:
        raise Forbidden(description="You cannot change your own email.")

    if "new_password" in data:
        if not Utils.is_admin() and "password" not in data:
            raise BadRequest(
                description="You must provide your current password.",
            )
        if not check_password_hash(
            user_in_db.encrypted_password, data["password"],
        ):
            raise BadRequest(description="Your current password is incorrect.")
        data["encrypted_password"] = generate_password_hash(
            data.pop("new_password"),
        )
        data.pop("password")

    try:
        for key in data:
            setattr(user_in_db, key, data[key])
        db.session.commit()
    except IntegrityError as e:
        msg = "A user already exists in database with the same email."
        raise Conflict(description=msg) from e

    return user_schema.dump(user_in_db), 200, {
        "Location": f"{request.base_url}/users/{user_in_db.id}",
    }


@Utils.require_auth
def delete(user_id: int) -> tuple:
    """Delete a user profile.

    Raises:
        Forbidden: If the user is not an admin or trying to delete another
        user's profile.

    Returns:
        tuple: A tuple containing None and the HTTP status code 204.

    """
    user = Utils.get_from_db(User, user_id)
    if not Utils.is_admin() or user.id != Utils.get_userid():
        raise Forbidden(description="You can only delete your own profile.")
    db.session.delete(user)
    db.session.commit()
    return None, 204

"""Arrow management endpoints for the API."""

# Copyright (c) 2025 oemf.jrmv.net

from flask import jsonify, make_response, request
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest, Forbidden

from app import db
from models.arrow import (
    Arrow,
    arrow_public_schema,
    arrow_schema,
    arrows_public_schema,
    arrows_schema,
)
from utils import Utils


@Utils.require_auth
def search(offset: int, limit: int, filters: object = None) -> tuple:
    """Search for arrows with optional filters.

    Raises:
        BadRequest: If the provided filters are invalid or if there is an issue
        with the database query.

    Returns:
        A tuple containing a list of arrows and the HTTP status code 200, along
        with headers for total count, limit, and offset.

    """
    try:
        query = Utils.build_query_filters(Arrow, filters)
        total = Arrow.query.filter(*query).count()
        arrows = Arrow.query.filter(*query)\
            .limit(limit).offset(offset).all()
    except AttributeError as e:
        msg = f"Something with filters `{filters}` is wrong..."
        raise BadRequest(description=msg) from e

    if not arrows:  # pragma: no cover
        return [], 204

    schema = arrows_schema if Utils.is_admin() else arrows_public_schema
    serialized = schema.dump(arrows)

    response = make_response(jsonify(serialized))
    response.headers["X-Total-Count"] = total
    response.headers["X-Limit"] = limit
    response.headers["X-Offset"] = offset

    return response


@Utils.require_auth
def post(arrow_data: object = None, **kwargs: object) -> tuple:
    """Create a new arrow.

    Raises:
        BadRequest: If the provided data is invalid.

    Returns:
        tuple: A tuple containing the created arrow and the HTTP status code
        201, along with a Location header pointing to the created arrow URL.

    """
    if arrow_data is None:
        arrow_data = kwargs.get("body", {})
    try:
        data = arrow_schema.load(arrow_data)
    except ValidationError as err:
        raise BadRequest(description=str(err)) from err
    if not hasattr(data, "user_id"):
        data["user_id"] = Utils.get_userid()
    arrow = Arrow(**data)
    db.session.add(arrow)
    db.session.commit()

    return arrow_schema.dump(arrow), 201, {
        "Location": f"{request.base_url}/arrows/{arrow.id}",
    }


@Utils.require_auth
def get(arrow_id: int) -> tuple:
    """Get an arrow by ID.

    Returns:
        tuple: A tuple containing the arrow data and the HTTP status code 200,
        along with a Location header pointing to the arrow URL.

    """
    arrow_in_db = Utils.get_from_db(Arrow, arrow_id)
    if Utils.is_admin():
        arrow = arrow_schema.dump(arrow_in_db)
    else:
        arrow = arrow_public_schema.dump(arrow_in_db)
    return arrow, 200, {
        "Location": f"{request.base_url}/arrows/{arrow_in_db.id}",
    }


@Utils.require_auth
def put(arrow_id: int, **kwargs: object) -> tuple:
    """Update an arrow.

    Raises:
        Forbidden: If the user is not an admin or trying to edit another user's
        arrow.
        BadRequest: If the provided data is invalid.

    Returns:
        tuple: A tuple containing the updated arrow and the HTTP status code
        200, along with a Location header pointing to the updated arrow URL.

    """
    arrow_in_db = Utils.get_from_db(Arrow, arrow_id)
    if not Utils.is_admin() and arrow_in_db.user_id != Utils.get_userid():
        raise Forbidden(description="You can only edit your own arrows.")
    arrow_data = kwargs.get("body", {})
    try:
        data = arrow_schema.load(arrow_data)
    except ValidationError as err:
        raise BadRequest(description=str(err)) from err
    for key in data:
        setattr(arrow_in_db, key, data[key])
    db.session.commit()

    return arrow_schema.dump(arrow_in_db), 200, {
        "Location": f"{request.base_url}/arrows/{arrow_in_db.id}",
    }


@Utils.require_auth
def delete(arrow_id: int) -> tuple:
    """Delete an arrow.

    Raises:
        Forbidden: If the user is not an admin or trying to delete another
        user's arrow.

    Returns:
        None: No content, HTTP status code 204.

    """
    arrow = Utils.get_from_db(Arrow, arrow_id)
    if not Utils.is_admin() and arrow.user_id != Utils.get_userid():
        raise Forbidden(description="You can only delete your own arrows.")
    db.session.delete(arrow)
    db.session.commit()
    return None, 204

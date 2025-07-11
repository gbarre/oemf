"""Utility functions and decorators for authentication and filtering."""

# Copyright (c) 2025 oemf.jrmv.net

from functools import wraps

import jwt
from flask import current_app, request
from sqlalchemy.exc import InvalidRequestError, StatementError
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, Unauthorized


class Utils:
    """Utility functions and decorators for authentication and filtering.

    This module contains helper methods used across the application, such as
    authentication decorators and SQLAlchemy query builders.

    """

    @staticmethod
    def get_from_db(object_class: object, o_id: int) -> object:
        """Get an object from the database by its class and ID.

        Args:
            object_class (object): The SQLAlchemy model class to query.
            o_id (int): The ID of the object to retrieve.

        Returns:
            object: The retrieved object if found.

        Raises:
            NotFound: If the object with the given ID does not exist.
            BadRequest: If there is an issue with the request or query.

        """
        try:
            object_in_db = object_class.query.get(o_id)
        except InvalidRequestError as e:  # pragma: no cover
            raise BadRequest from e
        except StatementError as e:  # pragma: no cover
            raise BadRequest(description=str(e)) from e

        if not object_in_db:
            name = object_class.__name__
            msg = f"The requested {name} `{o_id}` has not been found."
            raise NotFound(description=msg)
        return object_in_db

    @staticmethod
    def build_query_filters(model_class: object, filters: dict) -> list:
        """Build SQLAlchemy filters from a model class and a filters dict.

        Args:
            model_class (object): The SQLAlchemy model class to filter.
            filters (dict): A dictionary of filters where keys are field names
            and values are the filter values.

        Returns:
            A list of SQLAlchemy filter expressions.

        Raises:
            BadRequest if an invalid filter is provided.

        """
        query = []

        for query_filter, value in filters.items():
            if query_filter == "dateLost":
                field = model_class.date
                query.append(field >= value)
            elif query_filter == "dateFound":
                field = model_class.date
                query.append(field <= value)
            else:
                field = getattr(model_class, query_filter)
                query.append(field.ilike(f"%{value}%"))
        return query

    @staticmethod
    def is_admin() -> bool:
        """Check if the user is an admin.

        Returns:
            True if the user is an admin, False otherwise.

        """
        if not hasattr(request, "decoded_token"):
            return False

        email = request.decoded_token.get("sub")
        return email in current_app.config["ADMINS"]

    @staticmethod
    def get_userid() -> int:
        """Get the user ID from the decoded token.

        Returns:
            The user ID if available, otherwise -1.

        """
        if not hasattr(request, "decoded_token"):
            return None

        return int(request.decoded_token.get("userid", -1))

    @staticmethod
    def require_auth(view_func: object) -> object:
        """Require JWT authentication for a view function.

        Returns:
            object: The wrapped view function that requires authentication.

        Raises:
            Unauthorized if the token is missing, expired, or invalid.

        """

        def wrapper(*args: object, **kwargs: object) -> object:
            try:
                token = request.headers.get("Authorization")
                if not token:
                    raise Unauthorized(description="Token is missing")

                token = token.split(None, 1)[1].strip()
                algorithm = current_app.config["JWT"]["algorithm"]
                decoded_token = jwt.decode(
                    token,
                    current_app.config["JWT"]["secret"],
                    algorithms=[algorithm],
                )
                request.decoded_token = decoded_token
                return view_func(*args, **kwargs)
            except jwt.ExpiredSignatureError as e:
                raise Unauthorized(description="Token has expired") from e
            except jwt.InvalidTokenError as e:
                raise Unauthorized(description=str(e)) from e

        return wrapper

    @staticmethod
    def require_admin_token(view_func: object) -> object:
        """Require admin access for a view function.

        Returns:
            object: The wrapped view function with admin access check.

        """
        @Utils.require_auth
        @wraps(view_func)
        def wrapper(*args: object, **kwargs: object) -> object:
            if not Utils.is_admin():
                raise Forbidden(description="Admin access required")

            return view_func(*args, **kwargs)

        return wrapper

"""Defines custom exceptions and error handling for the API."""

# Copyright (c) 2025 oemf.jrmv.net

import connexion
from flask import jsonify
from werkzeug.exceptions import HTTPException


def render_exception(exception: Exception) -> tuple:
    """Render an exception into a JSON response.

    Args:
        exception (Exception): The exception to render.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.

    """
    if isinstance(exception, connexion.exceptions.ProblemException):
        error = f"{exception.status} {exception.title}"
        error_description = exception.detail
        code = exception.status
    else:
        if not isinstance(exception, HTTPException):  # pragma: nocover
            error_message = exception.args
            exception = HTTPException()
            if exception.name == "Unknown Error":
                error = "500 Internal Server Error"
                error_description = error_message[0]
                code = 500
        if exception.name != "Unknown Error":
            error = f"{exception.code} {exception.name}"
            error_description = exception.description
            code = exception.code

    response = {
        "error": error,
        "error_description": error_description,
    }

    return jsonify(response), code


class ConfigError(Exception):
    """Exception raised for configuration errors in the API."""


class NoContent(connexion.exceptions.ProblemException):
    """Exception raised when no content is available to return."""

    def __init__(self) -> None:
        """Initialize a NoContent exception."""
        self.status = 204
        self.title = ""
        self.detail = ""

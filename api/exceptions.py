import connexion
from werkzeug.exceptions import HTTPException
from flask import jsonify


def render_exception(exception):
    if isinstance(exception, connexion.exceptions.ProblemException):
        error = f"{exception.status} {exception.title}"
        error_description = exception.detail
        code = exception.status
    else:
        if not isinstance(exception, HTTPException):  # pragma: nocover
            error_message = exception.args
            exception = HTTPException()
            if exception.name == 'Unknown Error':
                error = '500 Internal Server Error'
                error_description = error_message[0]
                code = 500
        if exception.name != 'Unknown Error':
            error = f"{exception.code} {exception.name}"
            error_description = exception.description
            code = exception.code

    response = {
        'error': error,
        'error_description': error_description,
    }

    return jsonify(response), code


class ConfigError(Exception):
    pass


class NoContent(connexion.exceptions.ProblemException):
    def __init__(self):
        self.status = 204
        self.title = ''
        self.detail = ''

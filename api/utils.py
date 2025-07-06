from functools import wraps
from flask import request, current_app
from sqlalchemy.exc import InvalidRequestError, StatementError
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden
import jwt


class Utils:

    def get_from_db(object_class, id):
        try:
            object = object_class.query.get(id)
        except InvalidRequestError:  # pragma: no cover
            raise BadRequest
        except StatementError as e:  # pragma: no cover
            raise BadRequest(description=str(e))

        if not object:
            name = object_class.__name__
            msg = f'The requested {name} `{id}` has not been found.'
            raise NotFound(description=msg)
        else:
            return object

    def build_query_filters(model_class, filters):
        query = []

        for filter, value in filters.items():
            if filter == 'dateLost':
                field = getattr(model_class, 'date')
                query.append(field >= value)
            elif filter == 'dateFound':
                field = getattr(model_class, 'date')
                query.append(field <= value)
            else:
                field = getattr(model_class, filter)
                query.append(field.ilike(f'%{value}%'))
        return query

    def is_admin() -> bool:
        """Check if the user is an admin."""
        from flask import current_app, request

        if not hasattr(request, 'decoded_token'):
            return False

        email = request.decoded_token.get('sub')
        return email in current_app.config['ADMINS']

    def get_userid() -> int:
        """Get the user ID from the decoded token."""
        from flask import request

        if not hasattr(request, 'decoded_token'):
            return None

        return int(request.decoded_token.get('userid', -1))

    def require_auth(view_func):
        def wrapper(*args, **kwargs):
            try:
                token = request.headers.get('Authorization')
                if not token:
                    raise Unauthorized(description='Token is missing')

                token = token.split(None, 1)[1].strip()
                algorithm = current_app.config['JWT']['algorithm']
                decoded_token = jwt.decode(
                    token,
                    current_app.config['JWT']['secret'],
                    algorithms=[algorithm],
                )
                request.decoded_token = decoded_token
                return view_func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                raise Unauthorized(description='Token has expired')
            except jwt.InvalidTokenError as e:
                raise Unauthorized(description=str(e))

        return wrapper

    def require_admin_token(view_func):
        @Utils.require_auth
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not Utils.is_admin():
                raise Forbidden(description='Admin access required')

            return view_func(*args, **kwargs)

        return wrapper

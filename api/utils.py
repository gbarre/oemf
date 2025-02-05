from sqlalchemy.exc import InvalidRequestError, StatementError
from werkzeug.exceptions import BadRequest, NotFound


class Utils:

    def getObjectInDB(object_class, id):
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
            field = getattr(model_class, filter)
            query.append(field == value)
        return query

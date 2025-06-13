from flask import request
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

from app import db
from models.arrow import Arrow, arrow_schema, arrows_schema
from utils import Utils


# @require_auth
def search(offset, limit, filters):
    try:
        query = Utils.build_query_filters(Arrow, filters)
        arrows = Arrow.query.filter(*query)\
            .limit(limit).offset(offset).all()
    except AttributeError:
        msg = f'Something with filters `{filters}` is wrong...'
        raise BadRequest(description=msg)

    if not arrows:  # pragma: no cover
        return [], 204
    else:
        return arrows_schema.dump(arrows)


def post(arrow_data=None, **kwargs):
    if arrow_data is None:
        arrow_data = request.get_json()
    try:
        data = arrow_schema.load(arrow_data)
    except ValidationError as err:
        raise BadRequest(description=str(err))
    arrow = Arrow(**data)
    db.session.add(arrow)
    db.session.commit()

    return arrow_schema.dump(arrow), 201, {
        'Location': f'{request.base_url}/arrows/{arrow.id}',
    }


# @require_auth
def get(arrow_id):
    arrow_in_DB = Utils.getObjectInDB(Arrow, arrow_id)
    arrow = arrow_schema.dump(arrow_in_DB)
    return arrow, 200, {
        'Location': f'{request.base_url}/arrows/{arrow_in_DB.id}',
    }


# @require_auth
def put(arrow_id, **kwargs):
    arrow_in_DB = Utils.getObjectInDB(Arrow, arrow_id)
    arrow_data = kwargs.get('body', {})
    try:
        data = arrow_schema.load(arrow_data)
    except ValidationError as err:
        raise BadRequest(description=str(err))
    for key in data:
        setattr(arrow_in_DB, key, data[key])
    db.session.commit()

    return arrow_schema.dump(arrow_in_DB), 200, {
        'Location': f'{request.base_url}/arrows/{arrow_in_DB.id}',
    }


# @require_auth
def delete(arrow_id):
    arrow = Utils.getObjectInDB(Arrow, arrow_id)
    db.session.delete(arrow)
    db.session.commit()
    return None, 204

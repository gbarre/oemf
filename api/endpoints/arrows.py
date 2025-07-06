from flask import jsonify, make_response, request
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest, Forbidden

from app import db
from models.arrow import Arrow, arrow_schema, arrows_schema
from models.arrow import arrow_public_schema, arrows_public_schema
from utils import Utils


@Utils.require_auth
def search(offset, limit, filters):
    try:
        query = Utils.build_query_filters(Arrow, filters)
        total = Arrow.query.filter(*query).count()
        arrows = Arrow.query.filter(*query)\
            .limit(limit).offset(offset).all()
    except AttributeError:
        msg = f'Something with filters `{filters}` is wrong...'
        raise BadRequest(description=msg)

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
def post(arrow_data=None, **kwargs):
    if arrow_data is None:
        arrow_data = request.get_json()
    try:
        data = arrow_schema.load(arrow_data)
    except ValidationError as err:
        raise BadRequest(description=str(err))
    if not hasattr(data, 'user_id'):
        data['user_id'] = Utils.get_userid()
    arrow = Arrow(**data)
    db.session.add(arrow)
    db.session.commit()

    return arrow_schema.dump(arrow), 201, {
        'Location': f'{request.base_url}/arrows/{arrow.id}',
    }


@Utils.require_auth
def get(arrow_id):
    arrow_in_DB = Utils.get_from_db(Arrow, arrow_id)
    if Utils.is_admin():
        arrow = arrow_schema.dump(arrow_in_DB)
    else:
        arrow = arrow_public_schema.dump(arrow_in_DB)
    return arrow, 200, {
        'Location': f'{request.base_url}/arrows/{arrow_in_DB.id}',
    }


@Utils.require_auth
def put(arrow_id, **kwargs):
    arrow_in_DB = Utils.get_from_db(Arrow, arrow_id)
    if not Utils.is_admin() and arrow_in_DB.user_id != Utils.get_userid():
        raise Forbidden(description='You can only edit your own arrows.')
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


@Utils.require_auth
def delete(arrow_id):
    arrow = Utils.get_from_db(Arrow, arrow_id)
    if not Utils.is_admin() and arrow.user_id != Utils.get_userid():
        raise Forbidden(description='You can only delete your own arrows.')
    db.session.delete(arrow)
    db.session.commit()
    return None, 204

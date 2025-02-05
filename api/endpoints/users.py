from flask import request
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest, Conflict
from sqlalchemy.exc import IntegrityError

from app import db
# from auth import require_auth
from models.user import User, user_schema, users_schema
from utils import Utils


# @require_auth
def search(offset, limit, name=None):
    myfilters = {}
    if name is not None:
        myfilters['name'] = name
    try:
        query = Utils.build_query_filters(User, myfilters)
        users = User.query.filter(*query)\
            .limit(limit).offset(offset).all()
    except AttributeError:
        msg = f'Something with filters `{myfilters}` is wrong...'
        raise BadRequest(description=msg)

    if not users:  # pragma: no cover
        return [], 204
    else:
        return users_schema.dump(users)


# @require_auth
def post(user_data=None, **kwargs):
    if user_data is None:
        user_data = request.get_json()
    try:
        data = user_schema.load(user_data)
    except ValidationError as err:
        raise BadRequest(description=str(err))
    user = User(**data)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        msg = 'A user already exists in database with the same email.'
        raise Conflict(description=msg)

    return user_schema.dump(user), 201, {
        'Location': f'{request.base_url}/users/{user.id}',
    }


# @require_auth
def get(user_id):
    user_in_DB = Utils.getObjectInDB(User, user_id)
    user = user_schema.dump(user_in_DB)
    return user, 200, {
        'Location': f'{request.base_url}/users/{user_in_DB.id}',
    }


# @require_auth
def put(user_id, **kwargs):
    user_in_DB = Utils.getObjectInDB(User, user_id)
    user_data = kwargs.get('body', {})
    try:
        data = user_schema.load(user_data)
    except ValidationError as err:
        raise BadRequest(description=str(err))
    try:
        for key in data:
            setattr(user_in_DB, key, data[key])
        db.session.commit()
    except IntegrityError:
        msg = 'A user already exists in database with the same email.'
        raise Conflict(description=msg)

    return user_schema.dump(user_in_DB), 200, {
        'Location': f'{request.base_url}/users/{user_in_DB.id}',
    }


# @require_auth
def delete(user_id):
    user = Utils.getObjectInDB(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return None, 204

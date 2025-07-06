from flask import request
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest, Conflict, Forbidden
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

from app import db
from models.user import User, user_schema, users_schema
from utils import Utils


@Utils.require_admin_token
def search(offset, limit, filters):
    try:
        query = Utils.build_query_filters(User, filters)
        users = User.query.filter(*query)\
            .limit(limit).offset(offset).all()
    except AttributeError:
        msg = f'Something with filters `{filters}` is wrong...'
        raise BadRequest(description=msg)

    if not users:  # pragma: no cover
        return [], 200
    else:
        return users_schema.dump(users)


def post(user_data=None):
    if user_data is None:
        user_data = request.get_json()
    try:
        data = user_schema.load(user_data)
    except ValidationError as err:
        raise BadRequest(description=str(err))
    hashed_password = generate_password_hash(data['password'])
    data['encrypted_password'] = hashed_password
    data.pop('password', None)
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


@Utils.require_auth
def get(user_id):
    user_in_DB = Utils.get_from_db(User, user_id)
    if not Utils.is_admin() and user_in_DB.id != Utils.get_userid():
        raise Forbidden(description='You can only get your own profile.')
    user = user_schema.dump(user_in_DB)
    return user, 200, {
        'Location': f'{request.base_url}/users/{user_in_DB.id}',
    }


@Utils.require_auth
def put(user_id, **kwargs):
    user_in_DB = Utils.get_from_db(User, user_id)
    if not Utils.is_admin() and user_in_DB.id != Utils.get_userid():
        raise Forbidden(description='You can only edit your own profile.')
    user_data = kwargs.get('body', {})
    try:
        data = user_schema.load(user_data)
    except ValidationError as err:
        raise BadRequest(description=str(err))
    if not Utils.is_admin() and \
       'email' in data and \
       data['email'] != user_in_DB.email:
        raise Forbidden(description='You cannot change your own email.')
    if 'password' in data:
        data['encrypted_password'] = generate_password_hash(
            data.pop('password')
        )
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


@Utils.require_auth
def delete(user_id):
    user = Utils.get_from_db(User, user_id)
    if not Utils.is_admin() or user.id != Utils.get_userid():
        raise Forbidden(description='You can only delete your own profile.')
    db.session.delete(user)
    db.session.commit()
    return None, 204

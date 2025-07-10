from app import db, ma

from datetime import datetime
from marshmallow import fields


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    club = db.Column(db.String(255), nullable=False)
    encrypted_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', " \
               f"name='{self.name}', club='{self.club}')>"

    __table_args__ = {'extend_existing': True}


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    email = fields.String()
    name = fields.String()
    club = fields.String()
    password = fields.String(load_only=True)
    encrypted_password = fields.String(load_only=True)
    created_at = fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ", dump_only=True)


class UserPutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session

    email = fields.String()
    name = fields.String()
    club = fields.String()
    password = fields.String(load_only=True)
    newPassword = fields.String(load_only=True)
    encrypted_password = fields.String(load_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_put_schema = UserPutSchema()

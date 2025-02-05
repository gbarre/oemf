from app import db, ma
from models.arrow import Arrow  # noqa: F401

from datetime import datetime
from marshmallow import fields


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    club = db.Column(db.String, nullable=False)
    encrypted_password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relation avec Arrow
    arrows = db.relationship('Arrow', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', " \
               f"name='{self.name}', club='{self.club}')>"

    __table_args__ = {'extend_existing': True}


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session
        exclude = ('arrows',)

    id = fields.Integer(dump_only=True)
    email = fields.String()
    name = fields.String()
    club = fields.String()
    encrypted_password = fields.String(load_only=True)
    created_at = fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ", dump_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

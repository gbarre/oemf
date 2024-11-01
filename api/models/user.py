from sqlalchemy.orm import relationship
from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    club = db.Column(db.String, nullable=False)
    encrypted_password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relation avec Arrow
    arrows = relationship('Arrow', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', " \
               f"name='{self.name}', club='{self.club}')>"

from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app import db


# Enum pour le champ action dans Arrow
class ArrowAction(enum.Enum):
    found = "found"
    search = "search"


class Arrow(db.Model):
    __tablename__ = 'arrows'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
    )
    action = db.Column(
        db.Enum(ArrowAction),
        nullable=False,
    )
    date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    # Relations avec Shaft, Vane et Place
    shaft_id = db.Column(
        db.Integer,
        db.ForeignKey('shafts.id'),
    )
    place_id = db.Column(
        db.Integer,
        db.ForeignKey('places.id'),
    )

    shaft = relationship(
        'Shaft',
        back_populates='arrows',
        cascade="all, delete-orphan",
    )
    vanes = relationship(
        'Vane',
        secondary='arrow_vanes',
        back_populates='arrows',
    )
    place = relationship(
        'Place',
        back_populates='arrows',
        cascade="all, delete-orphan",
    )
    user = relationship(
        'User',
        back_populates='arrows',
    )

    def __repr__(self):
        return f"<Arrow(id={self.id}, action='{self.action}', " \
               f"date='{self.date}')>"


class Shaft(db.Model):
    __tablename__ = 'shafts'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    manufacturer = db.Column(
        db.String,
        nullable=False,
    )
    model = db.Column(
        db.String,
        nullable=False,
    )
    material = db.Column(
        db.String,
        nullable=True,
    )
    color = db.Column(
        db.String,
        nullable=True,
    )
    length = db.Column(
        db.Float,
        nullable=True,
    )

    # Relation avec Arrow
    arrows = relationship(
        'Arrow',
        back_populates='shaft',
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Shaft(id={self.id}, manufacturer='{self.manufacturer}', " \
               f"model='{self.model}')>"


class Vane(db.Model):
    __tablename__ = 'vanes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    manufacturer = db.Column(
        db.String,
        nullable=True,
    )
    color = db.Column(
        db.String,
        nullable=True,
    )

    # Relation many-to-many avec Arrow via une table d'association
    arrows = relationship(
        'Arrow',
        secondary='arrow_vanes',
        back_populates='vanes',
        )

    def __repr__(self):
        return f"<Vane(id={self.id}, manufacturer='{self.manufacturer}', " \
               f"color='{self.color}')>"


# Table d'association pour la relation many-to-many entre Arrow et Vane
arrow_vanes = db.Table(
    'arrow_vanes', db.Model.metadata,
    db.Column(
        'arrow_id',
        db.Integer,
        db.ForeignKey('arrows.id', ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        'vane_id',
        db.Integer,
        db.ForeignKey('vanes.id', ondelete="CASCADE"),
        primary_key=True,
    ),
)

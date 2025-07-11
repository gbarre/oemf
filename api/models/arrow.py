"""Arrow model and schema for the archery application."""

# Copyright (c) 2025 oemf.jrmv.net

import enum
from datetime import date
from typing import ClassVar

from marshmallow import fields

from app import db, ma


# Enum pour le champ action dans Arrow
class ArrowAction(enum.Enum):
    """Enum for the action field in Arrow model."""

    found = "found"
    lost = "lost"


class Arrow(db.Model):
    """Model representing an arrow in the archery application."""

    __tablename__ = "arrows"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    date = db.Column(
        db.Date,
        nullable=False,
        default=date.today,
    )
    action = db.Column(
        db.Enum(ArrowAction),
        nullable=False,
    )
    location = db.Column(
        db.String(255),
        nullable=False,
    )
    shaft_manufacturer = db.Column(
        db.String(255),
        nullable=True,
    )
    shaft_model = db.Column(
        db.String(255),
        nullable=True,
    )
    shaft_material = db.Column(
        db.String(255),
        nullable=True,
    )
    shaft_color = db.Column(
        db.String(255),
        nullable=True,
    )
    shaft_length = db.Column(
        db.Float,
        nullable=True,
    )
    vanes_count = db.Column(
        db.Integer,
        nullable=False,
    )
    vanes_color = db.Column(
        db.String(255),
        nullable=True,
    )
    point = db.Column(
        db.String(255),
        nullable=True,
    )
    nock = db.Column(
        db.String(255),
        nullable=True,
    )
    description = db.Column(
        db.Text,
        nullable=True,
    )

    def __repr__(self) -> str:
        """Return string representation of the Arrow model.

        Returns:
            A string representation of the Arrow object.

        """
        return (
            f"<Arrow(id={self.id}, action='{self.action}', "
            f"date='{self.date}')>"
        )

    __table_args__: ClassVar[dict[str, bool]] = {"extend_existing": True}


class ArrowSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Arrow model."""

    class Meta:
        """Meta class for ArrowSchema."""

        model = Arrow
        sqla_session = db.session
        include_fk = True

    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    date = fields.Date(format="%Y-%m-%d")
    action = fields.Enum(ArrowAction)


class ArrowPublicSchema(ma.SQLAlchemyAutoSchema):
    """Schema for public representation of Arrow model."""

    class Meta:
        """Meta class for ArrowPublicSchema."""

        model = Arrow
        sqla_session = db.session
        include_fk = True
        exclude = ("user_id",)

    id = fields.Integer(dump_only=True)
    date = fields.Date(format="%Y-%m-%d")
    action = fields.Enum(ArrowAction)
    location = fields.String()


arrow_schema = ArrowSchema()
arrows_schema = ArrowSchema(many=True)
arrow_public_schema = ArrowPublicSchema()
arrows_public_schema = ArrowPublicSchema(many=True)

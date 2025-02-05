from sqlalchemy.orm import relationship

from app import db


class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = db.Column(
        db.String,
        nullable=False,
    )
    description = db.Column(
        db.String,
        nullable=True,
    )

    # Relation avec Address (1-to-1) et Arrow (1-to-many)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    address = relationship(
        'Address',
        back_populates='place',
        cascade="all, delete-orphan",
        single_parent=True,
    )
    arrows = relationship(
        'Arrow',
        back_populates='place',
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Place(id={self.id}, name='{self.name}', " \
               f"description='{self.description}')>"


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    street = db.Column(
        db.String,
        nullable=False,
    )
    city = db.Column(
        db.String,
        nullable=False,
    )
    postal_code = db.Column(
        db.String,
        nullable=False,
    )
    country = db.Column(
        db.String,
        nullable=False,
    )
    latitude = db.Column(
        db.Float,
        nullable=True,
    )
    longitude = db.Column(
        db.Float,
        nullable=True,
    )

    # Relation avec Place
    place = relationship(
        'Place',
        back_populates='address',
        cascade="all, delete-orphan",
        single_parent=True,
    )

    def __repr__(self):
        return f"<Address(id={self.id}, street='{self.street}', " \
               f"city='{self.city}', country='{self.country}')>"

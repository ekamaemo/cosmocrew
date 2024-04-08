import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import relationship
from db_session import base
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class Users(base, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    planet_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("planets.id"))
    users = orm.relationship("Planets", back_populates='planet_id_users')

    def __init__(self, surname, name, email, password, planet_id):
        self.surname = surname
        self.name = name
        self.email = email
        self.hashed_password = password
        self.planet_id = planet_id

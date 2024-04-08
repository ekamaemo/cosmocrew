import sqlalchemy
import sqlalchemy.orm as orm
from werkzeug.security import generate_password_hash, check_password_hash
from db_session import base
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class Users(base, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    planet_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("planets.id"))
    users = orm.relationship("Planets", back_populates='planet_id_users')

    def __init__(self, name, email, password, planet_id):
        self.username = name
        self.email = email
        self.hashed_password = password
        self.planet_id = planet_id

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

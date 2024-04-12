import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import relationship
from db_session import base
from sqlalchemy_serializer import SerializerMixin


class Planets(base, SerializerMixin):
    __tablename__ = 'planets'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    planet_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    planet_image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    planet_id_users = relationship("Users", back_populates="users")
    planet_id_news = relationship("News", back_populates="news")

    def __init__(self, planet_name, planet_img):
        self.planet_name = planet_name
        self.planet_image = planet_img

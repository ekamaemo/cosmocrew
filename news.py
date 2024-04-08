import datetime
import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from db_session import base
from sqlalchemy_serializer import SerializerMixin


class News(base, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    url_source = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    planet_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("planets.id"))
    news = orm.relationship("Planets", back_populates='planet_id_news')

    def __init__(self, title, content, url_source, planet_id):
        self.title = title
        self.content = content
        self.url_source = url_source
        self.planet_id = planet_id

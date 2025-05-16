import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Genres(SqlAlchemyBase):
    __tablename__ = 'genres'

    genre_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    books = orm.relationship("Books", back_populates='genre')
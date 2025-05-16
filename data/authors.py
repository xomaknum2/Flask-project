import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Authors(SqlAlchemyBase):
    __tablename__ = 'authors'

    author_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    fullname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    birthday = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    portrait = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    short_biography = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    some_compositions = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    books = orm.relationship("Books", back_populates='author')

    def __init__(self, fullname, birthday, short_biography, some_compositions):
        self.fullname = fullname
        self.birthday = birthday
        self.short_biography = short_biography
        self.some_compositions = some_compositions

    def __repr__(self):
        return f"{self.fullname};{self.birthday};{self.short_biography};{self.some_compositions}"

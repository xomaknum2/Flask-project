import sqlalchemy
from sqlalchemy import orm
import base64

from .db_session import SqlAlchemyBase


class Books(SqlAlchemyBase):
    __tablename__ = 'books'

    book_id = sqlalchemy.Column(sqlalchemy.Integer,
                                primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    cover = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    discription = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    pages = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    year = sqlalchemy.Column(sqlalchemy.Integer)
    content_address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    how_many_like = sqlalchemy.Column(sqlalchemy.Integer)

    genre_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("genres.genre_id"))
    author_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("authors.author_id"))
    genre = orm.relationship('Genres', back_populates="books")
    author = orm.relationship('Authors', back_populates="books")

    books_progresses = orm.relationship("Book_progress", back_populates="book")

    def __repr__(self):
        return f"{self.title};{self.author_id};{self.genre_id};{base64.b16encode(self.cover).decode('utf-8')};{self.discription};{self.pages};{self.year};{self.how_many_like}"

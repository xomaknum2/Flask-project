from flask import Flask, render_template, redirect, request
from data.users import User
from data.books import Books
from data.authors import Authors
from data.genres import Genres
from data import db_session
from forms.user_registration import RegisterForm
from sqlalchemy.orm import joinedload
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.authorization import LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/', methods=['GET'])
def home_page():
    db_sess = db_session.create_session()
    books = db_sess.query(Books).options(joinedload(Books.author), joinedload(Books.genre)).all()
    return render_template("home_page.html", books=books, current_user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        user = User(
            username=form.username.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect("/")
    return render_template('registration.html', title='Регистрация', form=form)

@app.route('/books/<int:book_id>', methods=['GET'])
@login_required
def book_page(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Books).filter(Books.book_id==book_id).first()
    return render_template("book_page.html", book=book, current_user=current_user)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            print(request.data)
            return redirect("/")
        return render_template('authorization_form.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('authorization_form.html', form=form)

@app.route('/authors/<int:author_id>', methods=['GET'])
@login_required
def author_page(author_id):
    db_sess = db_session.create_session()
    author = db_sess.query(Authors).filter(Authors.author_id == author_id).first()
    return render_template("author_page.html", author=author)

@app.route('/allauthors', methods=['GET'])
@login_required
def all_authors():
    db_sess = db_session.create_session()
    authors = db_sess.query(Authors).all()
    return render_template("all_authors_page.html", authors=authors)

@app.route('/genres', methods=['GET'])
@login_required
def genres_page():
    db_sess = db_session.create_session()
    genres = db_sess.query(Genres).all()
    return render_template("genres_page.html", genres=genres)

@app.route('/genres/<int:genre_id>', methods=['GET'])
@login_required
def genre_page(genre_id):
    db_sess = db_session.create_session()
    genre = db_sess.query(Genres).filter(Genres.genre_id == genre_id).first()
    books = db_sess.query(Books).filter(Books.genre_id == genre_id).options(joinedload(Books.author), joinedload(Books.genre)).all()
    return render_template("genre_page.html", genre=genre, books=books)


def main():
    db_session.global_init("db/library.db")
    app.run(debug=True)


if __name__ == '__main__':
    main()

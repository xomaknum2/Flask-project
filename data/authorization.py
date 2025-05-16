from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
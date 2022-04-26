from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash


class RegisterForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])

    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[
                                       DataRequired(),
                                       EqualTo('password', message='Пароли не совпадают!')])
    submit = SubmitField("Submit")
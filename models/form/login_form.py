from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField


class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
    submit = SubmitField("Prisijungti")

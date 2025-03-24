from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import Length
from services.data_strength_services import email_strength, password_strength

class AdminLoginForm(FlaskForm):
    email = StringField("Email", validators=[Length(max=120), email_strength])
    password = PasswordField("Password", validators=[password_strength])
    submit = SubmitField("Prisijungti")

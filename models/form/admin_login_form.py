from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from services.email_strength_services import email_strength
from services.password_strength_services import password_strength

class AdminLoginForm(FlaskForm):
    email = StringField("Email", validators=[email_strength])
    password = PasswordField("Password", validators=[password_strength])
    submit = SubmitField("Prisijungti")

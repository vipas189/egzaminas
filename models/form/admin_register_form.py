from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from services.email_strength_services import email_strength
from services.password_strength_services import password_strength


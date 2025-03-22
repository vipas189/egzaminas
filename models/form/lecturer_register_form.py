from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import Length
from services.email_strength_services import email_strength
from services.password_strength_services import password_strength
from services.name_strength_services import name_strength
from services.last_name_strength_services import last_name_strength


class LecturerRegisterForm(FlaskForm):
    name = StringField("Name", validators=[Length(max=50), name_strength])
    last_name = StringField("LastName", validators=[Length(max=50), last_name_strength])
    email = StringField("Email", validators=[Length(max=120), email_strength])
    password = PasswordField("Password", validators=[password_strength])
    submit = SubmitField("Register")

from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import Length
from services.data_strength_services import (
    name_strength,
    last_name_strength,
    email_strength,
    password_strength,
)


class LecturerRegisterForm(FlaskForm):
    name = StringField("Name", validators=[Length(max=50), name_strength])
    last_name = StringField("LastName", validators=[Length(max=50), last_name_strength])
    email = StringField("Email", validators=[Length(max=120), email_strength])
    password = PasswordField("Password", validators=[password_strength])
    submit = SubmitField("Register")
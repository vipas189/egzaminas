from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from extensions import db
from models.program import Program
from wtforms_sqlalchemy import fields
from services.data_strength_services import (
    name_strength,
    last_name_strength,
    email_strength,
    password_strength,
)


class AddUserForm(FlaskForm):
    name = StringField("Name", validators=[name_strength])
    last_name = StringField("LastName", validators=[last_name_strength])
    email = StringField("Email", validators=[email_strength])
    password = PasswordField("Password", validators=[password_strength])
    role = SelectField(
        "Role",
        choices=[
            ("student", "Studentas"),
            ("lecturer", "Dėstytojas"),
            ("admin", "Administratorius"),
        ],
        validate_choice=[DataRequired()],
    )
    program = fields.QuerySelectField(
        "Program",
        query_factory=lambda: db.session.scalars(db.select(Program)).all(),
        get_label="name",
        allow_blank=True,
        validators=[DataRequired()],
    )
    # group = StringField("Group", validators=[Length(max=50), DataRequired()])

    submit = SubmitField("Patvirtinti")

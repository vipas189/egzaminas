from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

class InstructorForm(FlaskForm):
    name = StringField('Vardas', validators=[DataRequired()])
    last_name = StringField('Pavardė', validators=[DataRequired()])
    email = StringField('El. paštas', validators=[DataRequired(), Email()])
    department = StringField('Katedra', validators=[Optional()])
    position = StringField('Pareigos', validators=[Optional()])
    submit = SubmitField('Išsaugoti')

class InstructorAssignmentForm(FlaskForm):
    instructor_ids = SelectMultipleField('Pasirinkti dėstytojus', coerce=int, validators=[Optional()])
    submit = SubmitField('Priskirti dėstytojus')
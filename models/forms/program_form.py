from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ProgramForm(FlaskForm):
    name = StringField('Programos pavadinimas', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Aprašymas')
    submit = SubmitField('Išsaugoti programą')
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional

class AssessmentForm(FlaskForm):
    title = StringField('Pavadinimas', validators=[DataRequired()])
    description = TextAreaField('Aprašymas', validators=[Optional()])
    due_date = DateTimeField('Termino data', format='%d/%m/%Y %H:%M', validators=[DataRequired()])
    weight = FloatField('Svoris (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    module_id = SelectField('Modulis', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Išsaugoti atsiskaitymą')
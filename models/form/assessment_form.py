from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

class AssessmentForm(FlaskForm):
    title = StringField('Pavadinimas', validators=[DataRequired()])
    description = TextAreaField('Aprašymas')
    due_date = DateTimeField('Termino data', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    weight = FloatField('Svoris (%)', validators=[NumberRange(min=0, max=100)])
    module_id = SelectField('Modulis', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Išsaugoti atsiskaitymą')
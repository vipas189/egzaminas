from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class AssessmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateTimeField('Due Date', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    weight = FloatField('Weight (%)', validators=[NumberRange(min=0, max=100)])
    submit = SubmitField('Save Assessment')
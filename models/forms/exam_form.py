from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ExamForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    date = DateTimeField('Date and Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[NumberRange(min=30, max=240)])
    location = StringField('Location')
    weight = FloatField('Weight (%)', validators=[NumberRange(min=0, max=100)])
    submit = SubmitField('Save Exam')
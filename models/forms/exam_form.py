from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class ExamForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    date = DateTimeField('Date and Time', format='%d/%m/%Y %H:%M', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=30, max=240)])
    location = StringField('Location', validators=[Optional()])
    weight = FloatField('Weight (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    submit = SubmitField('Save Exam')
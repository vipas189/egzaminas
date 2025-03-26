from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import datetime

class ExamForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    # Pakeičiame DateTimeField į StringField, kad išvengtume validacijos problemų
    date = StringField('Date and Time', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=30, max=240)])
    location = StringField('Location', validators=[Optional()])
    weight = FloatField('Weight (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    submit = SubmitField('Save Exam')
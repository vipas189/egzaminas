from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ModuleForm(FlaskForm):
    name = StringField('Module Name', validators=[DataRequired(), Length(min=3, max=40)])
    description = TextAreaField('Description')
    credits = IntegerField('Credits', validators=[DataRequired(), NumberRange(min=1, max=30)])
    semester = SelectField('Semester', choices=[('Fall', 'Fall Semester'), ('Spring', 'Spring Semester')], 
                         validators=[DataRequired()])
    prerequisites = TextAreaField('Prerequisites')
    submit = SubmitField('Save Module')
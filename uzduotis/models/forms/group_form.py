from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class GroupFormationForm(FlaskForm):
    program_id = SelectField('Programa', coerce=int, validators=[DataRequired()])
    group_count = IntegerField('Grupių skaičius', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Formuoti grupes')

class GroupForm(FlaskForm):
    name = StringField('Grupės pavadinimas', validators=[DataRequired()])
    program_id = SelectField('Programa', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Išsaugoti grupę')
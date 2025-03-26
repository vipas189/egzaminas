from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class GroupFormationForm(FlaskForm):
    program_id = SelectField('Programa', coerce=int, validators=[DataRequired()])
    group_count = IntegerField('Grupių skaičius', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Formuoti grupes')

class GroupForm(FlaskForm):
    # Pašalintas name laukas, nes dabar grupės pavadinimas generuojamas automatiškai
    program_id = SelectField('Programa', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Išsaugoti grupę')
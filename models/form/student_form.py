# models/forms/student_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length

class StudentForm(FlaskForm):
    name = StringField('Vardas', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Pavardė', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('El. paštas', validators=[DataRequired(), Email()])
    program_id = SelectField('Programa', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Išsaugoti studentą')
    
class ModuleSelectionForm(FlaskForm):
    modules = SelectMultipleField('Pasirinkite modulius', coerce=int)
    submit = SubmitField('Išsaugoti pasirinkimus')
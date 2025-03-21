from flask_wtf import FlaskForm
from wtforms import FieldList, StringField, SubmitField
from wtforms.validators import DataRequired

class SolveTestForm(FlaskForm):
    answers = FieldList(StringField('Atsakymas', validators=[DataRequired()]))
    submit = SubmitField('Pateikti atsakymus')
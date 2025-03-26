from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SubmitField, SelectField, BooleanField, FieldList, FormField
from wtforms.validators import DataRequired, NumberRange

class TestQuestionOptionForm(FlaskForm):
    option_text = StringField('Atsakymo variantas', validators=[DataRequired()])
    is_correct = BooleanField('Teisingas')

class TestQuestionForm(FlaskForm):
    question_text = TextAreaField('Klausimas', validators=[DataRequired()])
    question_type = SelectField('Klausimo tipas', choices=[
        ('multiple_choice', 'Keli pasirinkimai'),
        ('true_false', 'Tiesa/Netiesa'),
        ('text', 'Tekstinis atsakymas')
    ], validators=[DataRequired()])
    points = IntegerField('Taškai', default=1, validators=[NumberRange(min=1)])
    options = FieldList(FormField(TestQuestionOptionForm), min_entries=2)

class TestForm(FlaskForm):
    title = StringField('Testo pavadinimas', validators=[DataRequired()])
    description = TextAreaField('Aprašymas')
    duration = IntegerField('Trukmė (min.)', validators=[DataRequired(), NumberRange(min=1, max=180)])
    passing_score = FloatField('Išlaikymo riba (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    weight = FloatField('Svoris vertinime (%)', validators=[NumberRange(min=0, max=100)])
    module_id = SelectField('Modulis', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Išsaugoti testą')
class SolveTestForm(FlaskForm):
    answers = FieldList(SelectField('Answer', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], validators=[DataRequired()]))
    submit = SubmitField('Submit Answers')
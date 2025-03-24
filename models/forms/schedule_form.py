from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TimeField, SubmitField
from wtforms.validators import DataRequired

class ScheduleForm(FlaskForm):
    day_of_week = SelectField('Day of Week', 
                            choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), 
                                    ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                                    ('Friday', 'Friday'), ('Saturday', 'Saturday'),
                                    ('Sunday', 'Sunday')],
                            validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()])
    end_time = TimeField('End Time', format='%H:%M', validators=[DataRequired()])
    location = StringField('Location')
    lecture_type = SelectField('Type', 
                             choices=[('Lecture', 'Lecture'), ('Lab', 'Laboratory'), 
                                     ('Seminar', 'Seminar'), ('Tutorial', 'Tutorial')],
                             validators=[DataRequired()])
    instructor_id = SelectField('Instructor', coerce=int)
    submit = SubmitField('Save Schedule')
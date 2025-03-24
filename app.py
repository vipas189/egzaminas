from flask import Flask
from config import Config
from extensions import db, migrate
from routes.__init__ import (
    routes,
)  # Importuoja routes funkcijos apibrėžimą iš __init__.py
from models.modules import Modules
from models.exam_mode import Exam
from models.schedule_model import Schedule
from models.assessments_model import Assessment
from models.program import Program
from models.students import Student
from models.instructor_model import Instructor
from models.student_calendar import StudentCalendar

# import tables cia kad jos veiktu!!!!

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)

# Registruoti maršrutus naudojant routes funkciją iš __init__.py
routes(app)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, redirect, url_for
from config import Config
from extensions import db, migrate, login_manager
from routes.__init__ import routes
from models.users import Users
from models.assessments_model import Assessment
from models.exam_mode import Exam
from models.instructor_model import Instructor
from models.modules import Modules
from models.program import Program, program_module
from models.schedule_model import Schedule
from models.student_calendar import StudentCalendar
from models.student_group import StudentGroup, student_group_membership
from models.test_model import (
    Test,
    TestAnswer,
    TestAttempt,
    TestQuestion,
    TestQuestionOption,
)


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = "login"


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("home"))


@login_manager.user_loader
def load_user(user_id):
    if user_id == "0":
        return Users(
            id=0,
            name=Config.ADMIN_NAME,
            last_name=Config.ADMIN_LAST_NAME,
            email=Config.ADMIN_EMAIL,
            password=Config.ADMIN_PASSWORD_HASH,
            role=Config.ADMIN_ROLE,
            profile_picture=Config.ADMIN_PROFILE_PICTURE,
        )
    return db.session.get(Users, int(user_id))


routes(app)


if __name__ == "__main__":
    app.run(debug=True)

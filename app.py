from flask import Flask
from config import Config
from extensions import db, migrate, login_manager
from routes.__init__ import routes
from liveserver import LiveServer
from livereload import Server
from models.answers import Answers
from models.assessments import Assignments
from models.groups import Groups
from models.module_prerequisites import module_prerequisites
from models.modules import Modules
from models.questions import Questions
from models.study_programs import StudyPrograms
from models.tests import Tests
from models.users import Users

app = Flask(__name__)
_ = LiveServer(app)
server = Server(app)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = "login"


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
        )
    return db.session.get(Users, int(user_id))


routes(app)


if __name__ == "__main__":
    server.serve(debug=True)

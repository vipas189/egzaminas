from flask import Flask
from config import Config
from extensions import db, migrate
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
routes(app)


if __name__ == "__main__":
    server.serve(debug=True)

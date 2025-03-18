from flask import Flask, render_template
from config import Config
from extensions import db, migrate
from models import student
from routes import student_routes


def main():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    student_routes.init_student_routes(app)
    app.run(debug=True)


if __name__ == "__main__":
    main()

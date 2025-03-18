from flask import render_template
import services.students_actions as st_act


def init_student_routes(app):
    @app.route("/students")
    def students():
        return render_template("students.html", students=st_act.view_students())

    @app.route("/create", methods=["GET", "POST"])
    def create():
        return


def init_home_route(app):
    @app.route("/")
    def home():
        return render_template("index.html")

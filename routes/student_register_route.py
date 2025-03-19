from flask import render_template
import services.student_register_services as student_exists


def student_register_route(app):
    @app.route("/student/register")
    def student_register():
        return render_template("student_register.html")

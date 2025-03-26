from flask import render_template, redirect, url_for
from flask_login import logout_user
from services.login_requirements import login_role_required


def panel_student_route(app):
    @app.route("/panel/student")
    @login_role_required("student")
    def panel_student():
        return render_template("panel_student.html")

    @app.route("/panel/student/logout", methods=["POST"])
    @login_role_required("student")
    def panel_student_logout():
        logout_user()
        return redirect(url_for("home"))

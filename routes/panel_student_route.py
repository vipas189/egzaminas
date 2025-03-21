from flask import render_template


def panel_student_route(app):
    @app.route("/panel")
    def panel_student():
        return render_template("panel_student.html")

from flask import render_template, redirect, url_for
from flask_login import logout_user, login_required
from services.login_requirements import login_role_required


def panel_lecturer_route(app):
    @app.route("/panel/lecturer")
    @login_role_required("lecturer")
    def panel_lecturer():
        return render_template("panel_lecturer.html")

    @app.route("/panel/lecturer/logout")
    @login_role_required("lecturer")
    def panel_lecturer_logout():
        logout_user()
        return redirect(url_for("home"))

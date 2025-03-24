from flask import render_template, redirect, url_for
from flask_login import logout_user
from services.login_requirements import login_role_required


def panel_superadmin_route(app):
    @app.route("/panel/superadmin")
    @login_role_required("superadmin")
    def panel_superadmin():
        return render_template("panel_superadmin.html")

    @app.route("/panel/superadmin/logout")
    @login_role_required("superadmin")
    def panel_superadmin_logout():
        logout_user()
        return redirect(url_for("home"))

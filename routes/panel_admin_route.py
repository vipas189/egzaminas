from flask import render_template, redirect, url_for
from flask_login import logout_user
from services.login_requirements import login_role_required


def panel_admin_route(app):
    @app.route("/panel/admin")
    @login_role_required("admin")
    def panel_admin():
        return render_template("panel_admin.html")

    @app.route("/panel/admin/logout")
    @login_role_required("admin")
    def panel_admin_logout():
        logout_user()
        return redirect(url_for("home"))

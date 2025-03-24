from flask import render_template, redirect, url_for
from flask_login import logout_user, login_required


def panel_admin_route(app):
    @app.route("/panel/admin")
    @login_required
    def panel_admin():
        return render_template("panel_admin.html")

    @app.route("/panel/admin/logout")
    @login_required
    def panel_admin_logout():
        logout_user()
        return redirect(url_for("home"))

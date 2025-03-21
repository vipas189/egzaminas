from flask import render_template


def panel_admin_route(app):
    @app.route("/panel")
    def panel_admin():
        return render_template("panel_admin.html")

from flask import render_template


def panel_route(app):
    @app.route("/panel")
    def panel():
        return render_template("panel.html")


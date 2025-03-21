from flask import render_template


def panel_lecturer_route(app):
    @app.route("/panel")
    def panel_lecturer():
        return render_template("panel_lecturer.html")

from flask import render_template, redirect, url_for, request


def panel_route(app):
    @app.route("/panel")
    def panel():
        return render_template("panel.html")
    
    @app.route("/")
    def add():
        return redirect(url_for("panel"))


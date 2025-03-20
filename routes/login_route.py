from flask import render_template


def login_route(app):
    @app.route("/login")
    def login():
        return render_template("login.html")

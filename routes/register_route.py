from flask import render_template


def register_route(app):
    @app.route("/register")
    def register():
        return render_template("register.html")

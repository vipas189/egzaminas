from flask import render_template

# import services.home_services as home_services   pavyzdys


def home_route(app):
    @app.route("/")
    def home():
        # home_services.home_view_users() pavyzdys
        return render_template("home.html")

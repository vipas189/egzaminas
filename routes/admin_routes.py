from flask import render_template
# # import services.home_services as home_services   pavyzdys


def admin_dashboard_route(app):
    @app.route("/admin")
    def dashboard():
        return render_template("admin.html")

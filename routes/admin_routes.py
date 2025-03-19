from flask import render_template
# import services.home_services as home_services   pavyzdys


def admin_routes(app):
    @app.route("/admin")
    def admin():
        
        return render_template("admin.html")

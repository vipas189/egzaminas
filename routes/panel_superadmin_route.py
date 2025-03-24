from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from config import Config


def panel_admin_route(app): 
    @app.route("/superadmin")
    @login_required
    def panel_superadmin():

        print(f"Current user: {current_user}")  # Debugging
        print(f"Is authenticated: {current_user.is_authenticated}")  # Debugging
        print(f"Current user email: {current_user.email}")  # Debugging
        print(f"Expected admin email: {Config.ADMIN_EMAIL}")

        if current_user.email != Config.ADMIN_EMAIL:
            print("Email doesn't match, redirecting to panel_admin")  # Debugging
            return redirect(url_for('panel_admin'))
        print("Rendering superadmin template")  # Debugging
        return render_template('panel_superadmin.html')
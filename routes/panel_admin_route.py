<<<<<<< HEAD
from flask import render_template


def panel_admin_route(app):
    @app.route("/panel")
    def panel_admin():
        return render_template("panel_admin.html")
=======
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import session
from models.admin import Admin
from models.form.admin_login_form import AdminLoginForm

def panel_admin_route(app):
    @app.route("/panel/admin", methods=['GET', 'POST'])
    def panel_admin():
        form = AdminLoginForm()
        form.validate_on_submit()
        return render_template('panel_admin.html', form = form) 
>>>>>>> origin/Admin_Management

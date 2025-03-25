from flask import render_template, redirect, url_for, flash
from flask_login import logout_user
from services.login_requirements import login_role_required
from models.form.create_user_form import AddUserForm
from models.form.student_register_form import StudentRegisterForm
from services.crud_services import create_user, read_users
from services.user_register_services import user_exists


def panel_superadmin_route(app):
    @app.route("/panel/superadmin")
    @login_role_required("superadmin")
    def panel_superadmin():
        form = AddUserForm()
        return render_template("panel_superadmin.html", form=form, users=read_users())

    @app.route("/panel/superadmin/logout", methods=["POST"])
    @login_role_required("superadmin")
    def panel_superadmin_logout():
        logout_user()
        return redirect(url_for("home"))

    @app.route("/panel/superadmin/create/user", methods=["POST"])
    @login_role_required("superadmin")
    def panel_superadmin_create_user():
        form = AddUserForm()
        error = False
        form.validate_on_submit()
        if form.name.errors:
            flash(form.name.errors[0], category="user_name_error")
            error = True
        if form.last_name.errors:
            flash(form.last_name.errors[0], category="user_last_name_error")
            error = True
        if form.email.errors:
            flash(form.email.errors[0], category="user_email_error")
            error = True
        if form.password.errors:
            flash(form.password.errors[0], category="user_password_error")
            error = True
        if form.program.errors and form.role.data == "student":
            flash(form.program.errors[0], category="user_program_error")
            error = True
        if not form.email.errors and user_exists(form.email.data):
            flash(
                "Toks el. pašto adresas jau egzistuoja. ", category="user_exists_error"
            )
            error = True
        if not form.program.errors and form.role.data in ["lecturer", "admin"]:
            flash(
                "Destytojai ir admin negali tureti studiju programos",
                category="user_program_error",
            )
            error = True
        if error:
            return redirect(url_for("panel_superadmin"))

        create_user(
            form.name.data,
            form.last_name.data,
            form.email.data,
            form.password.data,
            form.role.data,
            form.program.data.name if form.program.data else form.program.data,
        )
        return redirect(url_for("panel_superadmin"))

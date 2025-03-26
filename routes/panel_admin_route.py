from flask import render_template, redirect, url_for, flash, request
from flask_login import logout_user
from services.login_requirements import login_role_required
from models.form.admin_create_user_form import AddUserForm
from services.crud_services import (
    create_user,
    read_non_admin_users,
    update_user,
    remove_user,
)
from services.user_register_services import user_exists
from services.admin_dashboard_section_services import get_users_count, get_program_count


def panel_admin_route(app):
    @app.route("/panel/admin")
    @login_role_required("admin")
    def panel_admin():
        students_count = get_users_count("student")
        lecturer_count = get_users_count("lecturer")
        admin_count = get_users_count("admin")
        program_count = get_program_count()
        # group_count = get_group_count()
        form = AddUserForm()
        return render_template(
            "panel_admin.html",
            form=form,
            users=read_non_admin_users(),
            students_count=students_count,
            lecturer_count=lecturer_count,
            admin_count=admin_count,
            program_count=program_count,
        )

    @app.route("/panel/admin/logout", methods=["POST"])
    @login_role_required("admin")
    def panel_admin_logout():
        logout_user()
        return redirect(url_for("home"))

    @app.route("/panel/admin/create/user", methods=["POST"])
    @login_role_required("admin")
    def panel_admin_create_user():
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
                "Destytojai negali tureti studiju programos",
                category="user_program_error",
            )
            error = True
        if error:
            return redirect(url_for("panel_admin"))

        create_user(
            form.name.data,
            form.last_name.data,
            form.email.data,
            form.password.data,
            form.role.data,
            form.program.data.name if form.program.data else form.program.data,
        )
        return redirect(url_for("panel_admin"))

    @app.route("/panel/admin/update/user", methods=["POST"])
    @login_role_required("admin")
    def panel_admin_update_user():
        form = AddUserForm()
        user_id = request.form.get("user_id")
        error = False
        form.validate_on_submit()
        if form.name.errors:
            flash(form.name.errors[0], category=f"user_update_name_error{user_id}")
            error = True
        if form.last_name.errors:
            flash(
                form.last_name.errors[0],
                category=f"user_update_last_name_error{user_id}",
            )
            error = True
        if form.email.errors:
            flash(form.email.errors[0], category=f"user_update_email_error{user_id}")
            error = True
        if form.password.errors:
            flash(
                form.password.errors[0], category=f"user_update_password_error{user_id}"
            )
            error = True
        if form.program.errors and form.role.data == "student":
            flash(
                form.program.errors[0], category=f"user_update_program_error{user_id}"
            )
            error = True
        if not form.email.errors and user_exists(form.email.data):
            flash(
                "Toks el. pašto adresas jau egzistuoja. ",
                category=f"user_update_exists_error{user_id}",
            )
            error = True
        if not form.program.errors and form.role.data in ["lecturer", "admin"]:
            flash(
                "Destytojai negali tureti studiju programos",
                category=f"user_update_program_error{user_id}",
            )
            error = True
        if error:
            return redirect(url_for("panel_admin"))

        update_user(
            user_id,
            form.name.data,
            form.last_name.data,
            form.email.data,
            form.password.data,
            form.role.data,
            form.program.data.name if form.program.data else form.program.data,
        )
        return redirect(url_for("panel_admin"))

    @app.route("/panel/admin/delete/user", methods=["POST"])
    @login_role_required("admin")
    def panel_admin_delete_user():
        remove_user(request.form.get("user_id"))
        return redirect(url_for("panel_admin"))

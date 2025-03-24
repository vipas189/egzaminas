from models.form.student_register_form import StudentRegisterForm
from models.form.lecturer_register_form import LecturerRegisterForm
from flask import render_template, url_for, redirect, flash, get_flashed_messages
from services.user_register_services import user_exists, lecturer_add, student_add
from werkzeug.security import generate_password_hash
from services.study_programs_services import study_programs, study_program_name_to_id
from flask_login import login_user


def register_route(app):
    @app.route("/register")
    def register():
        active_tab = "student"
        tab_messages = get_flashed_messages(category_filter=["active_tab"])
        if tab_messages:
            active_tab = tab_messages[0]
        return render_template(
            "register.html",
            student_form=StudentRegisterForm(),
            lecturer_form=LecturerRegisterForm(),
            active_tab=active_tab,
            study_programs=study_programs(),
        )

    @app.route("/register/student", methods=["POST"])
    def register_student():
        error = False
        form = StudentRegisterForm()
        form.validate_on_submit()
        if form.name.errors:
            flash(form.name.errors[0], category="student_name")
            error = True
        if form.last_name.errors:
            flash(form.last_name.errors[0], category="student_last_name")
            error = True
        if form.email.errors:
            flash(form.email.errors[0], category="student_email")
            error = True
        if form.password.errors:
            flash(form.password.errors[0], category="student_password")
            error = True
        if form.study_program.errors:
            flash(form.study_program.errors[0], category="student_study_program")
            error = True
        if not form.email.errors and user_exists(form.email.data):
            flash("Toks el. pašto adresas jau egzistuoja. ", category="student_email")
            error = True
        if error:
            flash("student", category="active_tab")
            return redirect(url_for("register"))
        new_user = student_add(
            form.name.data,
            form.last_name.data,
            form.email.data,
            generate_password_hash(form.password.data),
            study_program_name_to_id(form.study_program.data),
        )
        login_user(new_user)
        return redirect(url_for("panel_admin"))

    @app.route("/register/lecturer", methods=["POST"])
    def register_lecturer():
        error = False
        form = LecturerRegisterForm()
        form.validate_on_submit()
        if form.name.errors:
            flash(form.name.errors[0], category="lecturer_name")
            error = True
        if form.last_name.errors:
            flash(form.last_name.errors[0], category="lecturer_last_name")
            error = True
        if form.email.errors:
            flash(form.email.errors[0], category="lecturer_email")
            error = True
        if form.password.errors:
            flash(form.password.errors[0], category="lecturer_password")
            error = True
        if not form.email.errors and user_exists(form.email.data):
            flash("Toks el. pašto adresas jau egzistuoja. ", category="lecturer_email")
            error = True
        if error:
            flash("lecturer", category="active_tab")
            return redirect(url_for("register"))
        new_user = lecturer_add(
            form.name.data,
            form.last_name.data,
            form.email.data,
            generate_password_hash(form.password.data),
        )
        login_user(new_user)
        return redirect(url_for("panel_admin"))

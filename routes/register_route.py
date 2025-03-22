from flask import render_template, url_for, redirect, flash
from models.form.student_register_form import StudentRegisterForm
from models.form.lecturer_register_form import LecturerRegisterForm
from services.student_register_services import student_exists, student_add
from services.lecturer_register_services import lecturer_exists, lecturer_add
from werkzeug.security import generate_password_hash


def register_route(app):
    @app.route("/register")
    def register():
        return render_template(
            "register.html",
            student_form=StudentRegisterForm(),
            lecturer_form=LecturerRegisterForm(),
        )

    @app.route("/register/student", methods=["POST"])
    def student():
        error = False
        form = StudentRegisterForm()
        form.validate_on_submit()
        if form.name.errors:
            flash(form.name.errors[0], category="student-name")
            error = True
        if form.last_name.errors:
            flash(form.last_name.errors[0], category="student-last_name")
            error = True
        if form.email.errors:
            flash(form.email.errors[0], category="student-email")
            error = True
        if form.password.errors:
            flash(form.password.errors[0], category="student-password")
            error = True
        if form.study_program.errors:
            flash(form.study_program.errors[0], category="student-study_program")
            error = True
        if not form.email.errors and student_exists(form.email.data):
            flash("Toks el. pašto adresas jau egzistuoja. ", category="student-email")
            error = True
        if error:
            return redirect(url_for("register"))
        student_add(
            form.name.data,
            form.last_name.data,
            form.email.data,
            generate_password_hash(form.password.data),
            form.study_program.data,
        )
        return redirect(url_for("panel_admin"))

    @app.route("/register/lecturer", methods=["POST"])
    def lecturer():
        error = False
        form = LecturerRegisterForm()
        form.validate_on_submit()
        if form.name.errors:
            flash(form.name.errors[0], category="lecturer-name")
            error = True
        if form.last_name.errors:
            flash(form.last_name.errors[0], category="lecturer-last_name")
            error = True
        if form.email.errors:
            flash(form.email.errors[0], category="lecturer-email")
            error = True
        if form.password.errors:
            flash(form.password.errors[0], category="lecturer-password")
            error = True
        if not form.email.errors and lecturer_exists(form.email.data):
            flash("Toks el. pašto adresas jau egzistuoja. ", category="lecturer-email")
            error = True
        if error:
            return redirect(url_for("register"))
        lecturer_add(
            form.name.data,
            form.last_name.data,
            form.email.data,
            generate_password_hash(form.password.data),
        )
        return redirect(url_for("panel_admin"))

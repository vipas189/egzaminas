from flask import render_template, url_for, redirect
from models.form.student_register_form import StudentRegisterForm
from models.form.lecturer_register_form import LecturerRegisterForm
from services.student_register_services import student_exists, student_add
from services.lecturer_register_services import lecturer_exists, lecturer_add


def get_form(form_type):
    form = {"student": StudentRegisterForm, "lecturer": LecturerRegisterForm}
    return form[form_type]()


def register_route(app):
    @app.route("/register")
    def register():
        return render_template(
            "register.html",
            student_form=get_form("student"),
            lecturer_form=get_form("lecturer"),
        )

    @app.route("/register/student", methods=["POST", "GET"])
    def student():
        form = get_form("student")
        if not form.validate_on_submit():
            return render_template(
                "register.html",
                student_form=form,
                lecturer_form=get_form("lecturer"),
            )
        if student_exists(form.email.data):
            form.errors["email"] = ["Email already exists"]
            return render_template(
                "register.html",
                student_form=form,
                lecturer_form=get_form("lecturer"),
            )
        student_add(form.email.data, form.password.data)
        return redirect(url_for("panel_admin"))

    @app.route("/register/lecturer", methods=["POST", "GET"])
    def lecturer():
        form = get_form("lecturer")
        if not form.validate_on_submit():
            return render_template(
                "register.html", student_form=get_form("student"), lecturer_form=form
            )
        if lecturer_exists(form.email.data):
            form.errors["email"] = ["Email already exists"]
            return render_template(
                "register.html",
                student_form=form,
                lecturer_form=get_form("lecturer"),
            )
        lecturer_add(form.email.data, form.password.data)
        return redirect(url_for("panel_admin"))

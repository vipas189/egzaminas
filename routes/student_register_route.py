from flask import render_template, request
from models.form.student_register_from import Student_register_form
from services.student_register_services import student_exists


def student_register_route(app):
    @app.route("/student/register", methods=["GET", "POST"])
    def student_register():
        form = Student_register_form()
        if request.method == "POST":
            if form.validate_on_submit():
                if student_exists(form.email.data):
                    form.errors["email"] = ["Email already exists"]
        else:
            form.errors.clear()
        return render_template("student_register.html", form=form)

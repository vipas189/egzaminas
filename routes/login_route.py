from flask import render_template, redirect, url_for, flash, get_flashed_messages
from flask_login import login_user
from models.form.login_form import LoginForm
from werkzeug.security import check_password_hash
from config import Config
from services.user_login_services import (
    user_exists,
    user_email_exists,
    user_failed_login,
    user_blocked,
)
from models.users import Users


def login_route(app):
    @app.route("/login")
    def login():
        active_tab = "student"
        tab_messages = get_flashed_messages(category_filter=["active_tab"])
        if tab_messages:
            active_tab = tab_messages[0]
        return render_template("login.html", active_tab=active_tab, form=LoginForm())

    @app.route("/login/student", methods=["POST"])
    def login_student():
        form = LoginForm()
        if user_blocked(form.email.data, "student"):
            flash(
                "Jusu paskyra buvo uzblokuota 1 minute", category="student_login_error"
            )
            flash("student", category="active_tab")
            return redirect(url_for("login"))
        student = user_exists(form.email.data, form.password.data, "student")
        if student:
            login_user(student)
            return redirect(url_for("panel_student"))
        elif user_email_exists(form.email.data, "student"):
            if user_failed_login(form.email.data, "student") >= 3:
                flash(
                    "Jusu paskyra buvo uzblokuota 1 minute",
                    category="student_login_error",
                )
                flash("student", category="active_tab")
                return redirect(url_for("login"))
        flash("Neteisingas el. paštas arba slaptažodis", category="student_login_error")
        flash("student", category="active_tab")
        return redirect(url_for("login"))

    @app.route("/login/lecturer", methods=["POST"])
    def login_lecturer():
        form = LoginForm()
        if user_blocked(form.email.data, "lecturer"):
            flash(
                "Jusu paskyra buvo uzblokuota 1 minute", category="lecturer_login_error"
            )
            flash("lecturer", category="active_tab")
            return redirect(url_for("login"))
        lecturer = user_exists(form.email.data, form.password.data, "lecturer")
        if lecturer:
            login_user(lecturer)
            return redirect(url_for("panel_lecturer"))
        elif user_email_exists(form.email.data, "lecturer"):
            if user_failed_login(form.email.data, "lecturer") >= 3:
                flash(
                    "Jusu paskyra buvo uzblokuota 1 minute",
                    category="lecturer_login_error",
                )
                flash("lecturer", category="active_tab")
                return redirect(url_for("login"))
        flash(
            "Neteisingas el. paštas arba slaptažodis", category="lecturer_login_error"
        )
        flash("lecturer", category="active_tab")
        return redirect(url_for("login"))

    @app.route("/login/admin", methods=["POST"])
    def login_admin():
        form = LoginForm()
        if user_blocked(form.email.data, "admin"):
            flash("Jusu paskyra buvo uzblokuota 1 minute", category="admin_login_error")
            flash("admin", category="active_tab")
            return redirect(url_for("login"))
        if form.email.data == Config.ADMIN_EMAIL and check_password_hash(
            Config.ADMIN_PASSWORD_HASH, form.password.data
        ):
            admin_user = Users(
                id=0,
                name=Config.ADMIN_NAME,
                last_name=Config.ADMIN_LAST_NAME,
                email=Config.ADMIN_EMAIL,
                password=Config.ADMIN_PASSWORD_HASH,
                role=Config.ADMIN_ROLE,
            )
            login_user(admin_user)
            return redirect(url_for("panel_superadmin"))
        admin = user_exists(form.email.data, form.password.data, "admin")
        if admin:
            login_user(admin)
            return redirect(url_for("panel_admin"))
        elif user_email_exists(form.email.data, "admin"):
            if user_failed_login(form.email.data, "admin") >= 3:
                flash(
                    "Jusu paskyra buvo uzblokuota 1 minute",
                    category="admin_login_error",
                )
                flash("lecturer", category="active_tab")
                return redirect(url_for("login"))
        flash("Neteisingas el. paštas arba slaptažodis", category="admin_login_error")
        flash("admin", category="active_tab")
        return redirect(url_for("login"))

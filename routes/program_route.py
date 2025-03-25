from flask import render_template, redirect, url_for, flash, request
from models.program import Program
from models.modules import Modules
from extensions import db
from models.form.program_form import ProgramForm


def program_routes(app):
    @app.route("/programs")
    def list_programs():
        programs = Program.query.all()
        return render_template("programs/index.html", programs=programs)

    @app.route("/programs/create", methods=["GET", "POST"])
    def create_program():
        form = ProgramForm()
        if form.validate_on_submit():
            program = Program(name=form.name.data, description=form.description.data)
            db.session.add(program)
            db.session.commit()
            flash("Programa sukurta sėkmingai!", "success")
            return redirect(url_for("list_programs"))
        return render_template("programs/create.html", form=form)

    @app.route("/programs/<int:id>")
    def view_program(id):
        program = Program.query.get_or_404(id)
        return render_template("programs/view.html", program=program)

    @app.route("/programs/<int:id>/modules", methods=["GET", "POST"])
    def program_modules(id):
        program = Program.query.get_or_404(id)
        if request.method == "POST":
            # Apdoroti modulių priskyrimą programai
            module_ids = request.form.getlist("modules")
            modules = Modules.query.filter(Modules.id.in_(module_ids)).all()
            program.modules = modules
            db.session.commit()
            flash("Moduliai priskirti programai sėkmingai!", "success")
            return redirect(url_for("view_program", id=program.id))

        # Gauti visus modulius
        all_modules = Modules.query.all()
        return render_template(
            "programs/modules.html", program=program, modules=all_modules
        )

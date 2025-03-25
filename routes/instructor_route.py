from flask import render_template, redirect, url_for, flash
from models.instructor_model import Instructor
from models.modules import Modules
from models.assessments_model import Assessment
from models.schedule_model import Schedule
from models.student_module import student_module
from models.student_calendar import StudentCalendar
from models.form.instructor_form import InstructorForm
from models.form.assessment_form import AssessmentForm
from extensions import db


def instructor_routes(app):
    @app.route("/instructors")
    def list_instructors():
        instructors = Instructor.query.all()
        return render_template("instructors/index.html", instructors=instructors)

    @app.route("/instructors/create", methods=["GET", "POST"])
    def create_instructor():
        form = InstructorForm()

        if form.validate_on_submit():
            instructor = Instructor(
                name=form.name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                department=form.department.data,
                position=form.position.data,
            )
            db.session.add(instructor)
            db.session.commit()
            flash("Dėstytojas sėkmingai sukurtas!", "success")
            return redirect(url_for("list_instructors"))

        return render_template("instructors/create.html", form=form)

    @app.route("/instructors/<int:id>")
    def view_instructor(id):
        instructor = Instructor.query.get_or_404(id)

        # Gauti modulius, kuriuos dėsto instruktorius
        modules = instructor.modules

        # Gauti tvarkaraščio įrašus, kur dėstytojas yra priskirtas
        schedules = Schedule.query.filter_by(instructor_id=id).all()

        return render_template(
            "instructors/view.html",
            instructor=instructor,
            modules=modules,
            schedules=schedules,
        )

    @app.route("/instructors/<int:id>/edit", methods=["GET", "POST"])
    def edit_instructor(id):
        instructor = Instructor.query.get_or_404(id)
        form = InstructorForm(obj=instructor)

        if form.validate_on_submit():
            form.populate_obj(instructor)
            db.session.commit()
            flash("Dėstytojas sėkmingai atnaujintas!", "success")
            return redirect(url_for("view_instructor", id=instructor.id))

        return render_template(
            "instructors/edit.html", form=form, instructor=instructor
        )

    @app.route("/instructors/<int:id>/delete", methods=["POST"])
    def delete_instructor(id):
        instructor = Instructor.query.get_or_404(id)
        db.session.delete(instructor)
        db.session.commit()
        flash("Dėstytojas sėkmingai ištrintas!", "success")
        return redirect(url_for("list_instructors"))

    # Maršrutai atsiskaitymų valdymui dėstytojams
    @app.route("/instructors/<int:id>/assessments")
    def instructor_assessments(id):
        instructor = Instructor.query.get_or_404(id)

        # Gauti modulius, kuriuos dėsto instruktorius
        modules = instructor.modules

        # Gauti visus atsiskaitymus, susijusius su tais moduliais
        assessments = []
        for module in modules:
            module_assessments = Assessment.query.filter_by(module_id=module.id).all()
            assessments.extend(module_assessments)

        return render_template(
            "instructors/assessments.html",
            instructor=instructor,
            assessments=assessments,
            modules=modules,
        )

    @app.route("/instructors/<int:id>/assessments/add", methods=["GET", "POST"])
    def instructor_add_assessment(id):
        instructor = Instructor.query.get_or_404(id)

        # Gauti modulius, kuriuos dėsto instruktorius
        instructor_modules = instructor.modules

        # Jei nėra modulių, nukreipti atgal su pranešimu
        if not instructor_modules:
            flash(
                "Negalite pridėti atsiskaitymų, nes nesate priskirtas jokiam moduliui.",
                "warning",
            )
            return redirect(url_for("instructor_assessments", id=id))

        # Kurti formą ir pridėti dinamišką modulių pasirinkimą
        form = AssessmentForm()
        form.module_id.choices = [(m.id, m.name) for m in instructor_modules]

        if form.validate_on_submit():
            assessment = Assessment(
                module_id=form.module_id.data,
                title=form.title.data,
                description=form.description.data,
                due_date=form.due_date.data,
                weight=form.weight.data,
            )
            db.session.add(assessment)

            # Atnaujinti studentų kalendorius su nauju atsiskaitymu
            update_student_calendars_for_assessment(assessment)

            db.session.commit()
            flash(
                "Atsiskaitymas sėkmingai pridėtas ir įtrauktas į studentų kalendorius!",
                "success",
            )
            return redirect(url_for("instructor_assessments", id=instructor.id))

        return render_template(
            "instructors/add_assessment.html", form=form, instructor=instructor
        )

    @app.route(
        "/instructors/<int:instructor_id>/assessments/<int:assessment_id>/edit",
        methods=["GET", "POST"],
    )
    def instructor_edit_assessment(instructor_id, assessment_id):
        instructor = Instructor.query.get_or_404(instructor_id)
        assessment = Assessment.query.get_or_404(assessment_id)

        # Patikrinti, ar šis atsiskaitymas priklauso moduliui, kurį dėsto dėstytojas
        module = Modules.query.get(assessment.module_id)
        if module not in instructor.modules:
            flash("Jūs neturite teisės redaguoti šį atsiskaitymą!", "danger")
            return redirect(url_for("instructor_assessments", id=instructor_id))

        form = AssessmentForm(obj=assessment)

        if form.validate_on_submit():
            old_due_date = assessment.due_date
            form.populate_obj(assessment)

            # Jei pasikeitė data, atnaujinti studentų kalendorius
            if old_due_date != assessment.due_date:
                # Pirmiausia ištrinti senus kalendoriaus įrašus
                StudentCalendar.query.filter_by(
                    event_type="assessment", module_id=assessment.module_id
                ).filter(StudentCalendar.title.like(f"%{assessment.title}%")).delete()

                # Sukurti naujus kalendoriaus įrašus
                update_student_calendars_for_assessment(assessment)

            db.session.commit()
            flash(
                "Atsiskaitymas sėkmingai atnaujintas ir studentų kalendoriai atnaujinti!",
                "success",
            )
            return redirect(url_for("instructor_assessments", id=instructor_id))

        return render_template(
            "instructors/edit_assessment.html",
            form=form,
            instructor=instructor,
            assessment=assessment,
        )

    @app.route(
        "/instructors/<int:instructor_id>/assessments/<int:assessment_id>/cancel",
        methods=["POST"],
    )
    def instructor_cancel_assessment(instructor_id, assessment_id):
        instructor = Instructor.query.get_or_404(instructor_id)
        assessment = Assessment.query.get_or_404(assessment_id)

        # Patikrinti, ar šis atsiskaitymas priklauso moduliui, kurį dėsto dėstytojas
        module = Modules.query.get(assessment.module_id)
        if module not in instructor.modules:
            flash("Jūs neturite teisės atšaukti šį atsiskaitymą!", "danger")
            return redirect(url_for("instructor_assessments", id=instructor_id))

        # Pirmiausia ištrinti susijusius kalendoriaus įrašus
        StudentCalendar.query.filter_by(
            event_type="assessment", module_id=assessment.module_id
        ).filter(StudentCalendar.title.like(f"%{assessment.title}%")).delete()

        # Tada ištrinti patį atsiskaitymą
        db.session.delete(assessment)
        db.session.commit()

        flash(
            "Atsiskaitymas sėkmingai atšauktas ir pašalintas iš studentų kalendorių!",
            "success",
        )
        return redirect(url_for("instructor_assessments", id=instructor_id))

    # Funkcija atnaujinti studentų kalendorius
    def update_student_calendars_for_assessment(assessment):
        # Gauti modulį
        module = Modules.query.get(assessment.module_id)

        # Gauti visus studentus, kurie pasirinko šį modulį
        students = module.enrolled_students

        # Pridėti atsiskaitymą į kiekvieno studento kalendorių
        for student in students:
            calendar_item = StudentCalendar(
                student_id=student.id,
                title=f"{module.name} - {assessment.title}",
                description=assessment.description,
                event_type="assessment",
                module_id=module.id,
                date=assessment.due_date.date(),
                start_time=assessment.due_date.time() if assessment.due_date else None,
            )
            db.session.add(calendar_item)

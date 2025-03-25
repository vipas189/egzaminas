from flask import render_template, redirect, url_for, flash
from models.modules import Modules
from models.schedule_model import Schedule
from models.assessments_model import Assessment
from models.exam_mode import Exam
from models.instructor_model import Instructor
from models.form.module_form import ModuleForm
from models.form.schedule_form import ScheduleForm
from models.form.assessment_form import AssessmentForm
from models.form.exam_form import ExamForm
from models.form.instructor_form import InstructorAssignmentForm
from models.student_calendar import StudentCalendar
from extensions import db


def module_route(app):
    # List all modules
    @app.route("/modules")
    def list_modules():
        modules = Modules.query.all()
        return render_template("modules/index.html", modules=modules)

    # Create new module
    @app.route("/modules/create", methods=["GET", "POST"])
    def create_module():
        form = ModuleForm()
        if form.validate_on_submit():
            module = Modules(
                name=form.name.data,
                description=form.description.data,
                credits=form.credits.data,
                semester=form.semester.data,
                prerequisites=form.prerequisites.data,
            )
            db.session.add(module)
            db.session.commit()
            flash("Module created successfully!", "success")
            return redirect(url_for("view_module", id=module.id))
        return render_template("modules/create.html", form=form)

    # View module details
    @app.route("/modules/<int:id>")
    def view_module(id):
        module = Modules.query.get_or_404(id)
        schedules = Schedule.query.filter_by(module_id=id).all()
        assessments = Assessment.query.filter_by(module_id=id).all()
        exams = Exam.query.filter_by(module_id=id).all()
        instructors = module.instructors
        students = module.enrolled_students

        return render_template(
            "modules/view.html",
            module=module,
            schedules=schedules,
            assessments=assessments,
            exams=exams,
            instructors=instructors,
            students=students,
        )

    # Edit module
    @app.route("/modules/<int:id>/edit", methods=["GET", "POST"])
    def edit_module(id):
        module = Modules.query.get_or_404(id)
        form = ModuleForm(obj=module)

        if form.validate_on_submit():
            form.populate_obj(module)
            db.session.commit()
            flash("Module updated successfully!", "success")
            return redirect(url_for("view_module", id=module.id))

        return render_template("modules/edit.html", form=form, module=module)

    # Delete module
    @app.route("/modules/<int:id>/delete", methods=["POST"])
    def delete_module(id):
        module = Modules.query.get_or_404(id)
        db.session.delete(module)
        db.session.commit()
        flash("Module deleted successfully!", "success")
        return redirect(url_for("list_modules"))

    # Schedule management
    @app.route("/modules/<int:id>/schedules/add", methods=["GET", "POST"])
    def add_schedule(id):
        module = Modules.query.get_or_404(id)
        form = ScheduleForm()

        # Pridėti dėstytojų pasirinkimą
        form.instructor_id.choices = [(0, "None")] + [
            (i.id, f"{i.name} {i.last_name}") for i in Instructor.query.all()
        ]

        if form.validate_on_submit():
            schedule = Schedule(
                module_id=id,
                day_of_week=form.day_of_week.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                location=form.location.data,
                lecture_type=form.lecture_type.data,
            )

            # Pridėti dėstytoją, jei pasirinktas
            if form.instructor_id.data > 0:
                schedule.instructor_id = form.instructor_id.data

            db.session.add(schedule)
            db.session.commit()

            # Atnaujinti studentų kalendorius
            update_student_calendars_for_schedule(schedule)

            flash(
                "Schedule added successfully and student calendars updated!", "success"
            )
            return redirect(url_for("view_module", id=id))

        return render_template("modules/add_schedule.html", form=form, module=module)

    @app.route(
        "/modules/<int:module_id>/schedules/<int:schedule_id>/edit",
        methods=["GET", "POST"],
    )
    def edit_schedule(module_id, schedule_id):
        module = Modules.query.get_or_404(module_id)
        schedule = Schedule.query.get_or_404(schedule_id)

        if schedule.module_id != module_id:
            flash("Invalid schedule for this module!", "danger")
            return redirect(url_for("view_module", id=module_id))

        form = ScheduleForm(obj=schedule)
        form.instructor_id.choices = [(0, "None")] + [
            (i.id, f"{i.name} {i.last_name}") for i in Instructor.query.all()
        ]

        if form.validate_on_submit():
            old_day = schedule.day_of_week
            old_start_time = schedule.start_time

            form.populate_obj(schedule)
            if form.instructor_id.data == 0:
                schedule.instructor_id = None

            # Jei pasikeitė diena arba laikas, atnaujinti studentų kalendorius
            if old_day != schedule.day_of_week or old_start_time != schedule.start_time:
                # Pirmiausia ištrinti senus kalendoriaus įrašus
                StudentCalendar.query.filter_by(
                    event_type="schedule", module_id=module_id
                ).filter(
                    StudentCalendar.title.like(
                        f"%{module.name}%{schedule.lecture_type}%"
                    )
                ).delete()

                # Sukurti naujus kalendoriaus įrašus
                update_student_calendars_for_schedule(schedule)

            db.session.commit()
            flash(
                "Schedule updated successfully and student calendars updated!",
                "success",
            )
            return redirect(url_for("view_module", id=module_id))

        # Nustatyti pradinę dėstytojo reikšmę
        if schedule.instructor_id:
            form.instructor_id.data = schedule.instructor_id
        else:
            form.instructor_id.data = 0

        return render_template(
            "modules/edit_schedule.html", form=form, module=module, schedule=schedule
        )

    @app.route(
        "/modules/<int:module_id>/schedules/<int:schedule_id>/delete", methods=["POST"]
    )
    def delete_schedule(module_id, schedule_id):
        schedule = Schedule.query.get_or_404(schedule_id)

        if schedule.module_id != module_id:
            flash("Invalid schedule for this module!", "danger")
            return redirect(url_for("view_module", id=module_id))

        # Pirmiausia ištrinti susijusius kalendoriaus įrašus
        module = Modules.query.get(module_id)
        StudentCalendar.query.filter_by(
            event_type="schedule", module_id=module_id
        ).filter(
            StudentCalendar.title.like(f"%{module.name}%{schedule.lecture_type}%")
        ).delete()

        db.session.delete(schedule)
        db.session.commit()
        flash(
            "Schedule deleted successfully and removed from student calendars!",
            "success",
        )
        return redirect(url_for("view_module", id=module_id))

    # Assessment management
    @app.route("/modules/<int:id>/assessments/add", methods=["GET", "POST"])
    def add_assessment(id):
        module = Modules.query.get_or_404(id)
        form = AssessmentForm()

        if form.validate_on_submit():
            assessment = Assessment(
                module_id=id,
                title=form.title.data,
                description=form.description.data,
                due_date=form.due_date.data,
                weight=form.weight.data,
            )
            db.session.add(assessment)

            # Atnaujinti studentų kalendorius
            update_student_calendars_for_assessment(assessment)

            db.session.commit()
            flash(
                "Assessment added successfully and student calendars updated!",
                "success",
            )
            return redirect(url_for("view_module", id=id))

        return render_template("modules/add_assessment.html", form=form, module=module)

    @app.route(
        "/modules/<int:module_id>/assessments/<int:assessment_id>/edit",
        methods=["GET", "POST"],
    )
    def edit_assessment(module_id, assessment_id):
        module = Modules.query.get_or_404(module_id)
        assessment = Assessment.query.get_or_404(assessment_id)

        if assessment.module_id != module_id:
            flash("Invalid assessment for this module!", "danger")
            return redirect(url_for("view_module", id=module_id))

        form = AssessmentForm(obj=assessment)

        if form.validate_on_submit():
            old_due_date = assessment.due_date
            form.populate_obj(assessment)

            # Jei pasikeitė data, atnaujinti studentų kalendorius
            if old_due_date != assessment.due_date:
                # Pirmiausia ištrinti senus kalendoriaus įrašus
                StudentCalendar.query.filter_by(
                    event_type="assessment", module_id=module_id
                ).filter(StudentCalendar.title.like(f"%{assessment.title}%")).delete()

                # Sukurti naujus kalendoriaus įrašus
                update_student_calendars_for_assessment(assessment)

            db.session.commit()
            flash(
                "Assessment updated successfully and student calendars updated!",
                "success",
            )
            return redirect(url_for("view_module", id=module_id))

        return render_template(
            "modules/edit_assessment.html",
            form=form,
            module=module,
            assessment=assessment,
        )

    @app.route(
        "/modules/<int:module_id>/assessments/<int:assessment_id>/delete",
        methods=["POST"],
    )
    def delete_assessment(module_id, assessment_id):
        assessment = Assessment.query.get_or_404(assessment_id)

        if assessment.module_id != module_id:
            flash("Invalid assessment for this module!", "danger")
            return redirect(url_for("view_module", id=module_id))

        # Pirmiausia ištrinti susijusius kalendoriaus įrašus
        StudentCalendar.query.filter_by(
            event_type="assessment", module_id=module_id
        ).filter(StudentCalendar.title.like(f"%{assessment.title}%")).delete()

        db.session.delete(assessment)
        db.session.commit()
        flash(
            "Assessment deleted successfully and removed from student calendars!",
            "success",
        )
        return redirect(url_for("view_module", id=module_id))

    # Exam management
    @app.route("/modules/<int:id>/exams/add", methods=["GET", "POST"])
    def add_exam(id):
        module = Modules.query.get_or_404(id)
        form = ExamForm()

        if form.validate_on_submit():
            exam = Exam(
                module_id=id,
                title=form.title.data,
                description=form.description.data,
                date=form.date.data,
                duration=form.duration.data,
                location=form.location.data,
                weight=form.weight.data,
            )
            db.session.add(exam)

            # Atnaujinti studentų kalendorius
            update_student_calendars_for_exam(exam)

            db.session.commit()
            flash("Exam added successfully and student calendars updated!", "success")
            return redirect(url_for("view_module", id=id))

        return render_template("modules/add_exam.html", form=form, module=module)

    @app.route(
        "/modules/<int:module_id>/exams/<int:exam_id>/edit", methods=["GET", "POST"]
    )
    def edit_exam(module_id, exam_id):
        module = Modules.query.get_or_404(module_id)
        exam = Exam.query.get_or_404(exam_id)

        if exam.module_id != module_id:
            flash("Invalid exam for this module!", "danger")
            return redirect(url_for("view_module", id=module_id))

        form = ExamForm(obj=exam)

        if form.validate_on_submit():
            old_date = exam.date
            form.populate_obj(exam)

            # Jei pasikeitė data, atnaujinti studentų kalendorius
            if old_date != exam.date:
                # Pirmiausia ištrinti senus kalendoriaus įrašus
                StudentCalendar.query.filter_by(
                    event_type="exam", module_id=module_id
                ).filter(StudentCalendar.title.like(f"%{exam.title}%")).delete()

                # Sukurti naujus kalendoriaus įrašus
                update_student_calendars_for_exam(exam)

            db.session.commit()
            flash("Exam updated successfully and student calendars updated!", "success")
            return redirect(url_for("view_module", id=module_id))

        return render_template(
            "modules/edit_exam.html", form=form, module=module, exam=exam
        )

    @app.route("/modules/<int:module_id>/exams/<int:exam_id>/delete", methods=["POST"])
    def delete_exam(module_id, exam_id):
        exam = Exam.query.get_or_404(exam_id)

        if exam.module_id != module_id:
            flash("Invalid exam for this module!", "danger")
            return redirect(url_for("view_module", id=module_id))

        # Pirmiausia ištrinti susijusius kalendoriaus įrašus
        StudentCalendar.query.filter_by(event_type="exam", module_id=module_id).filter(
            StudentCalendar.title.like(f"%{exam.title}%")
        ).delete()

        db.session.delete(exam)
        db.session.commit()
        flash(
            "Exam deleted successfully and removed from student calendars!", "success"
        )
        return redirect(url_for("view_module", id=module_id))

    # Instructors management
    @app.route("/modules/<int:id>/instructors", methods=["GET", "POST"])
    def module_instructors(id):
        module = Modules.query.get_or_404(id)
        form = InstructorAssignmentForm()

        # Gauti visus dėstytojus
        all_instructors = Instructor.query.all()
        # Pakeisti, kaip formuojamas pasirinkimo tekstas - pridėjome katedrą, kad būtų aiškiau
        form.instructor_ids.choices = [
            (i.id, f"{i.name} {i.last_name} ({i.department or 'Be katedros'})")
            for i in all_instructors
        ]

        if form.validate_on_submit():
            instructor_ids = form.instructor_ids.data
            instructors = Instructor.query.filter(
                Instructor.id.in_(instructor_ids)
            ).all()
            module.instructors = instructors
            db.session.commit()
            flash("Instructors assigned successfully!", "success")
            return redirect(url_for("view_module", id=module.id))

        # Nustatyti pradines pasirinkimo reikšmes
        if not form.instructor_ids.data and module.instructors:
            form.instructor_ids.data = [i.id for i in module.instructors]

        return render_template(
            "modules/instructors.html",
            form=form,
            module=module,
            instructors=all_instructors,
        )

    # Funkcijos studentų kalendoriams atnaujinti
    def update_student_calendars_for_schedule(schedule):
        module = Modules.query.get(schedule.module_id)
        students = module.enrolled_students

        for student in students:
            calendar_item = StudentCalendar(
                student_id=student.id,
                title=f"{module.name} - {schedule.lecture_type}",
                description=f"Modulis: {module.name}, Tipas: {schedule.lecture_type}",
                event_type="schedule",
                module_id=module.id,
                start_time=schedule.start_time,
                end_time=schedule.end_time,
                location=schedule.location,
            )
            db.session.add(calendar_item)

    def update_student_calendars_for_assessment(assessment):
        module = Modules.query.get(assessment.module_id)
        students = module.enrolled_students

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

    def update_student_calendars_for_exam(exam):
        module = Modules.query.get(exam.module_id)
        students = module.enrolled_students

        for student in students:
            calendar_item = StudentCalendar(
                student_id=student.id,
                title=f"{module.name} - {exam.title}",
                description=exam.description,
                event_type="exam",
                module_id=module.id,
                date=exam.date.date(),
                start_time=exam.date.time() if exam.date else None,
                end_time=None,  # Vėliau galima apskaičiuoti pabaigos laiką pagal trukmę
                location=exam.location,
            )
            db.session.add(calendar_item)

from flask import Blueprint, render_template, redirect, url_for, flash, request
from models.students import Student, StudentGrade
from models.program import Program
from models.modules import Modules
from models.schedule_model import Schedule
from models.assessments_model import Assessment
from models.exam_mode import Exam
from models.student_calendar import StudentCalendar
from models.forms.student_form import StudentForm, ModuleSelectionForm
from models.forms.program_form import ProgramForm
from extensions import db
from datetime import datetime


def student_routes(app):
    # Studentų maršrutai
    @app.route("/students")
    def list_students():
        students = Student.query.all()
        return render_template("students/index.html", students=students)

    @app.route("/students/create", methods=["GET", "POST"])
    def create_student():
        form = StudentForm()
        # Užpildyti programų pasirinkimą
        form.program_id.choices = [(p.id, p.name) for p in Program.query.all()]

        if form.validate_on_submit():
            student = Student(
                name=form.name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                program_id=form.program_id.data,
            )
            db.session.add(student)
            db.session.commit()
            flash("Studentas sukurtas sėkmingai!", "success")
            return redirect(url_for("list_students"))
        return render_template("students/create.html", form=form)

    @app.route("/students/<int:id>")
    def view_student(id):
        student = Student.query.get_or_404(id)
        return render_template("students/view.html", student=student)

    @app.route("/students/<int:id>/select_modules", methods=["GET", "POST"])
    def select_modules(id):
        student = Student.query.get_or_404(id)
        form = ModuleSelectionForm()

        # Gauti modulius, kurie priklauso studento programai
        if student.program:
            program_modules = student.program.modules
            # Nustatyti pasirinkimų sąrašą
            form.modules.choices = [
                (m.id, f"{m.name} ({m.credits} kr.)") for m in program_modules
            ]
        else:
            program_modules = []
            form.modules.choices = []
            flash(
                "Studentas nepriskirtas jokiai programai, todėl negalima pasirinkti modulių.",
                "warning",
            )

        if form.validate_on_submit():
            selected_module_ids = form.modules.data

            # Patikrinti išankstinius reikalavimus ir tvarkaraščio konfliktus
            can_enroll, error_msg = check_enrollment_validity(
                student, selected_module_ids
            )

            if can_enroll:
                # Priskirti modulius studentui
                selected_modules = Modules.query.filter(
                    Modules.id.in_(selected_module_ids)
                ).all()
                student.selected_modules = selected_modules

                # Sukurti asmeninį kalendorių studentui
                create_student_calendar(student, selected_modules)

                db.session.commit()
                flash(
                    "Moduliai pasirinkti sėkmingai ir pridėti į asmeninį kalendorių!",
                    "success",
                )
                return redirect(url_for("student_calendar", id=student.id))
            else:
                flash(error_msg, "danger")

        # Nustatyti pradines pasirinkimo reikšmes pagal studento jau pasirinktus modulius
        if not form.modules.data and student.selected_modules:
            form.modules.data = [m.id for m in student.selected_modules]

        return render_template(
            "students/select_modules.html",
            form=form,
            student=student,
            program_modules=program_modules,
        )

    @app.route("/students/<int:id>/calendar")
    def student_calendar(id):
        student = Student.query.get_or_404(id)
        calendar_items = get_student_calendar_items(student)

        # Sugrupuoti kalendoriaus įrašus pagal tipą
        schedules = [item for item in calendar_items if item["type"] == "schedule"]
        assessments = [item for item in calendar_items if item["type"] == "assessment"]
        exams = [item for item in calendar_items if item["type"] == "exam"]

        return render_template(
            "students/calendar.html",
            student=student,
            schedules=schedules,
            assessments=assessments,
            exams=exams,
        )

    # Funkcija tikrinti ar studentas gali registruotis į modulius
    def check_enrollment_validity(student, module_ids):
        if not module_ids:
            return True, ""

        modules = Modules.query.filter(Modules.id.in_(module_ids)).all()

        # Patikrinti išankstinius reikalavimus
        for module in modules:
            if module.prerequisites:
                # Tikriname, ar studentas turi reikalingus išankstinius modulius
                prereq_names = [
                    name.strip() for name in module.prerequisites.split(",")
                ]

                # Gauti visus studento jau išklausytus modulius
                completed_modules = [
                    m for m in student.selected_modules if m.id not in module_ids
                ]
                completed_names = [m.name for m in completed_modules]

                # Tikriname ar visi reikalingi išankstiniai moduliai yra išklausyti
                for prereq in prereq_names:
                    if prereq and prereq not in completed_names:
                        return (
                            False,
                            f"Trūksta išankstinio reikalavimo: {prereq} moduliui {module.name}",
                        )

        # Patikrinti tvarkaraščio konfliktus
        schedules = []
        for module in modules:
            module_schedules = Schedule.query.filter_by(module_id=module.id).all()
            schedules.extend(module_schedules)

        # Tikrinti konfliktus tarp tvarkaraščių
        for i, s1 in enumerate(schedules):
            for s2 in schedules[i + 1 :]:
                if s1.day_of_week == s2.day_of_week:
                    # Patikrinti ar laikai persidengia
                    if s1.start_time <= s2.end_time and s1.end_time >= s2.start_time:
                        module1 = Modules.query.get(s1.module_id)
                        module2 = Modules.query.get(s2.module_id)
                        return (
                            False,
                            f"Tvarkaraščio konfliktas: {module1.name} ir {module2.name} modulių užsiėmimai vyksta tuo pačiu metu ({s1.day_of_week}, {s1.start_time.strftime('%H:%M')}-{s1.end_time.strftime('%H:%M')})!",
                        )

        return True, ""

    # Funkcija sukurti asmeninį kalendorių studentui
    def create_student_calendar(student, modules):
        # Pirmiausia išvalyti visus esamus kalendoriaus įrašus
        StudentCalendar.query.filter_by(student_id=student.id).delete()

        # Sukurti naujus kalendoriaus įrašus
        for module in modules:
            # Pridėti tvarkaraščio įrašus
            schedules = Schedule.query.filter_by(module_id=module.id).all()
            for schedule in schedules:
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

            # Pridėti atsiskaitymų datas
            assessments = Assessment.query.filter_by(module_id=module.id).all()
            for assessment in assessments:
                calendar_item = StudentCalendar(
                    student_id=student.id,
                    title=f"{module.name} - {assessment.title}",
                    description=assessment.description,
                    event_type="assessment",
                    module_id=module.id,
                    date=assessment.due_date.date(),
                    start_time=(
                        assessment.due_date.time() if assessment.due_date else None
                    ),
                )
                db.session.add(calendar_item)

            # Pridėti egzaminų datas
            exams = Exam.query.filter_by(module_id=module.id).all()
            for exam in exams:
                calendar_item = StudentCalendar(
                    student_id=student.id,
                    title=f"{module.name} - {exam.title}",
                    description=exam.description,
                    event_type="exam",
                    module_id=module.id,
                    date=exam.date.date(),
                    start_time=exam.date.time() if exam.date else None,
                    end_time=(
                        (exam.date.time() if exam.date else None)
                        if not exam.duration
                        else None
                    ),  # Vėliau galima apskaičiuoti pabaigos laiką
                    location=exam.location,
                )
                db.session.add(calendar_item)

        # Išsaugoti kalendoriaus įrašus
        db.session.commit()

    # Funkcija gauti studento kalendoriaus įrašus
    def get_student_calendar_items(student):
        calendar_items = []

        # Pirma bandyti gauti įrašus iš StudentCalendar modelio
        db_calendar_items = StudentCalendar.query.filter_by(student_id=student.id).all()

        if db_calendar_items:
            for item in db_calendar_items:
                module = Modules.query.get(item.module_id)

                calendar_item = {
                    "type": item.event_type,
                    "module": module.name if module else "Nežinomas modulis",
                    "title": item.title,
                    "description": item.description,
                    "date": item.date,
                    "start_time": item.start_time,
                    "end_time": item.end_time,
                    "location": item.location,
                }
                calendar_items.append(calendar_item)
        else:
            # Jei nėra StudentCalendar įrašų, sukurti laikinus iš studento pasirinktų modulių
            modules = student.selected_modules

            for module in modules:
                # Pridėti tvarkaraščio įrašus
                schedules = Schedule.query.filter_by(module_id=module.id).all()
                for schedule in schedules:
                    calendar_items.append(
                        {
                            "type": "schedule",
                            "module": module.name,
                            "title": f"{module.name} - {schedule.lecture_type}",
                            "description": f"Modulis: {module.name}, Tipas: {schedule.lecture_type}",
                            "day": schedule.day_of_week,
                            "start_time": schedule.start_time,
                            "end_time": schedule.end_time,
                            "location": schedule.location,
                            "lecture_type": schedule.lecture_type,
                        }
                    )

                # Pridėti atsiskaitymų datas
                assessments = Assessment.query.filter_by(module_id=module.id).all()
                for assessment in assessments:
                    calendar_items.append(
                        {
                            "type": "assessment",
                            "module": module.name,
                            "title": assessment.title,
                            "description": assessment.description,
                            "date": assessment.due_date,
                            "weight": assessment.weight,
                        }
                    )

                # Pridėti egzaminų datas
                exams = Exam.query.filter_by(module_id=module.id).all()
                for exam in exams:
                    calendar_items.append(
                        {
                            "type": "exam",
                            "module": module.name,
                            "title": exam.title,
                            "description": exam.description,
                            "date": exam.date,
                            "duration": exam.duration,
                            "location": exam.location,
                            "weight": exam.weight,
                        }
                    )

        # Surūšiuoti kalendoriaus įrašus
        # Pirma pagal datą/dieną, tada pagal pradžios laiką
        calendar_items.sort(
            key=lambda x: (
                (
                    x.get("date", datetime.max.date())
                    if x.get("date")
                    else datetime.max.date()
                ),
                x.get("day", "Zzz") if x.get("day") else "Zzz",
                (
                    x.get("start_time", datetime.max.time())
                    if x.get("start_time")
                    else datetime.max.time()
                ),
            )
        )

        return calendar_items
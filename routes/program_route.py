from flask import Blueprint, render_template, redirect, url_for, flash, request
from models.students import Student
from models.program import Program
from models.modules import Modules
from models.schedule_model import Schedule
from models.forms.student_form import StudentForm, ModuleSelectionForm
from extensions import db
from models.forms.program_form import ProgramForm

def student_routes(app):
    @app.route('/students')
    def list_students():


@app.route('/programs')
def list_programs():
    programs = Program.query.all()
    return render_template('programs/index.html', programs=programs)

@app.route('/programs/create', methods=['GET', 'POST'])
def create_program():
    form = ProgramForm()
    if form.validate_on_submit():
        program = Program(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(program)
        db.session.commit()
        flash('Programa sukurta sėkmingai!', 'success')
        return redirect(url_for('list_programs'))
    return render_template('programs/create.html', form=form)

@app.route('/programs/<int:id>')
def view_program(id):
    program = Program.query.get_or_404(id)
    return render_template('programs/view.html', program=program)

@app.route('/programs/<int:id>/modules', methods=['GET', 'POST'])
def program_modules(id):
    program = Program.query.get_or_404(id)
    if request.method == 'POST':
        # Apdoroti modulių priskyrimą programai
        module_ids = request.form.getlist('modules')
        modules = Modules.query.filter(Modules.id.in_(module_ids)).all()
        program.modules = modules
        db.session.commit()
        flash('Moduliai priskirti programai sėkmingai!', 'success')
        return redirect(url_for('view_program', id=program.id))
    
    # Gauti visus modulius
    all_modules = Modules.query.all()
    return render_template('programs/modules.html', program=program, modules=all_modules)

# Studentų maršrutai
@app.route('/students')
def list_students():
    students = Student.query.all()
    return render_template('students/index.html', students=students)

@app.route('/students/create', methods=['GET', 'POST'])
def create_student():
    form = StudentForm()
    # Užpildyti programų pasirinkimą
    form.program_id.choices = [(p.id, p.name) for p in Program.query.all()]
    
    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            program_id=form.program_id.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Studentas sukurtas sėkmingai!', 'success')
        return redirect(url_for('list_students'))
    return render_template('students/create.html', form=form)

@app.route('/students/<int:id>')
def view_student(id):
    student = Student.query.get_or_404(id)
    return render_template('students/view.html', student=student)

@app.route('/students/<int:id>/select_modules', methods=['GET', 'POST'])
def select_modules(id):
    student = Student.query.get_or_404(id)
    form = ModuleSelectionForm()
    
    # Gauti modulius, kurie priklauso studento programai
    program_modules = student.program.modules if student.program else []
    
    # Nustatyti pasirinkimų sąrašą
    form.modules.choices = [(m.id, m.name) for m in program_modules]
    
    if form.validate_on_submit():
        selected_module_ids = form.modules.data
        
        # Patikrinti išankstinius reikalavimus ir tvarkaraščio konfliktus
        can_enroll, error_msg = check_enrollment_validity(student, selected_module_ids)
        
        if can_enroll:
            # Priskirti modulius studentui
            selected_modules = Modules.query.filter(Modules.id.in_(selected_module_ids)).all()
            student.selected_modules = selected_modules
            db.session.commit()
            flash('Moduliai pasirinkti sėkmingai!', 'success')
            return redirect(url_for('view_student', id=student.id))
        else:
            flash(error_msg, 'danger')
    
    # Nustatyti pradines pasirinkimo reikšmes pagal studento jau pasirinktus modulius
    if not form.modules.data and student.selected_modules:
        form.modules.data = [m.id for m in student.selected_modules]
    
    return render_template('students/select_modules.html', form=form, student=student)

# Funkcija tikrinti ar studentas gali registruotis į modulius
def check_enrollment_validity(student, module_ids):
    modules = Modules.query.filter(Modules.id.in_(module_ids)).all()
    
    # Patikrinti išankstinius reikalavimus
    for module in modules:
        if module.prerequisites:
            # Čia reikėtų įgyvendinti logiką, kuri tikrina, ar studentas atitinka išankstinius reikalavimus
            # Paprastam pavyzdžiui tiesiog grąžiname True
            pass
    
    # Patikrinti tvarkaraščio konfliktus
    schedules = []
    for module in modules:
        module_schedules = Schedule.query.filter_by(module_id=module.id).all()
        schedules.extend(module_schedules)
    
    # Tikrinti konfliktus tarp tvarkaraščių
    for i, s1 in enumerate(schedules):
        for s2 in schedules[i+1:]:
            if s1.day_of_week == s2.day_of_week:
                # Patikrinti ar laikai persidengia
                if (s1.start_time <= s2.end_time and s1.end_time >= s2.start_time):
                    return False, f"Tvarkaraščio konfliktas: {s1.module.name} ir {s2.module.name} modulių užsiėmimai vyksta tuo pačiu metu!"
    
    return True, ""
from flask import render_template, redirect, url_for, flash, request
from models.student_group import StudentGroup
from models.program import Program
from models.students import Student
from models.forms.group_form import GroupFormationForm, GroupForm
from extensions import db
import math
import datetime

def generate_group_name(program_name):
    """
    Sugeneruoja grupės pavadinimą pagal programos pavadinimą ir dabartinius metus.
    Paima pirmo ir antro žodžio pirmas dvi raides ir prideda paskutinius du metų skaičius.
    """
    words = program_name.split()
    
    # Gauti pirmo žodžio pirmas dvi raides
    first_word = words[0][:2].upper()
    
    # Gauti antro žodžio pirmas dvi raides (jei antras žodis egzistuoja)
    second_word = words[1][:2].upper() if len(words) > 1 else "XX"
    
    # Gauti dabartinius metus (paskutinius du skaičius)
    current_year = str(datetime.datetime.now().year)[-2:]
    
    # Sujungti viską į vieną pavadinimą
    return f"{first_word}{second_word}{current_year}"

def group_routes(app):
    # Atvaizduoja visų grupių sąrašą
    @app.route('/groups')
    def list_groups():
        groups = StudentGroup.query.all()
        return render_template('groups/index.html', groups=groups)

    # Sukuria naują grupę su automatiniu pavadinimo generavimu
    @app.route('/groups/create', methods=['GET', 'POST'])
    def create_group():
        form = GroupForm()
        form.program_id.choices = [(p.id, p.name) for p in Program.query.all()]
        
        if form.validate_on_submit():
            # Pavadinimas generuojamas automatiškai pagal programos pavadinimą
            program = Program.query.get(form.program_id.data)
            group_name = generate_group_name(program.name)
            
            group = StudentGroup(
                name=group_name,
                program_id=form.program_id.data
            )
            db.session.add(group)
            db.session.commit()
            flash('Grupė sukurta sėkmingai!', 'success')
            return redirect(url_for('list_groups'))
            
        return render_template('groups/create.html', form=form)

    # Automatiškai formuoja grupes programai su nauja pavadinimų logika
    @app.route('/groups/form', methods=['GET', 'POST'])
    def form_groups():
        form = GroupFormationForm()
        form.program_id.choices = [(p.id, p.name) for p in Program.query.all()]
        
        if form.validate_on_submit():
            program_id = form.program_id.data
            group_count = form.group_count.data
            
            # Gauti visus studentus iš pasirinktos programos
            students = Student.query.filter_by(program_id=program_id).all()
            
            if not students:
                flash(f'Programoje nėra studentų', 'warning')
                return redirect(url_for('form_groups'))
            
            # Pašalinti visas esamas grupes šioje programoje
            existing_groups = StudentGroup.query.filter_by(program_id=program_id).all()
            for group in existing_groups:
                db.session.delete(group)
            
            # Sukurti naujas grupes
            program = Program.query.get(program_id)
            total_students = len(students)
            students_per_group = math.ceil(total_students / group_count)
            
            # Sugeneruoti bazinį grupės pavadinimą
            base_name = generate_group_name(program.name)
            
            # Padalinti studentus į grupes
            groups = []
            for i in range(group_count):
                # Pridėti raidę prie grupės pavadinimo, jei grupių daugiau nei viena
                if group_count > 1:
                    suffix = chr(97 + i)  # 'a', 'b', 'c', ...
                    group_name = f"{base_name}{suffix}"
                else:
                    group_name = base_name
                
                group = StudentGroup(
                    name=group_name,
                    program_id=program_id
                )
                db.session.add(group)
                db.session.flush()  # Gauti grupės ID
                groups.append(group)
            
            # Priskirti studentus į grupes
            for i, student in enumerate(students):
                group_index = min(i // students_per_group, group_count - 1)
                groups[group_index].students.append(student)
            
            db.session.commit()
            flash(f'Sukurtos {group_count} grupės ir paskirstyti {total_students} studentai', 'success')
            return redirect(url_for('list_groups'))
            
        return render_template('groups/form_groups.html', form=form)

    # Peržiūri specifinės grupės informaciją
    @app.route('/groups/<int:id>')
    def view_group(id):
        group = StudentGroup.query.get_or_404(id)
        return render_template('groups/view.html', group=group)

    # Redaguoja grupės informaciją
    @app.route('/groups/<int:id>/edit', methods=['GET', 'POST'])
    def edit_group(id):
        group = StudentGroup.query.get_or_404(id)
        form = GroupForm(obj=group)
        form.program_id.choices = [(p.id, p.name) for p in Program.query.all()]
        
        if form.validate_on_submit():
            # Naudojame įvestą pavadinimą
            form.populate_obj(group)
            db.session.commit()
            flash('Grupė atnaujinta sėkmingai!', 'success')
            return redirect(url_for('view_group', id=group.id))
            
        return render_template('groups/edit.html', form=form, group=group)

    # Ištrina grupę
    @app.route('/groups/<int:id>/delete', methods=['POST'])
    def delete_group(id):
        group = StudentGroup.query.get_or_404(id)
        db.session.delete(group)
        db.session.commit()
        flash('Grupė ištrinta sėkmingai!', 'success')
        return redirect(url_for('list_groups'))

    # Valdo grupės studentų sąrašą
    @app.route('/groups/<int:id>/students', methods=['GET', 'POST'])
    def manage_group_students(id):
        group = StudentGroup.query.get_or_404(id)
        
        if request.method == 'POST':
            student_ids = request.form.getlist('students')
            students = Student.query.filter(Student.id.in_(student_ids)).all()
            
            # Atnaujinti studentų sąrašą
            group.students = students
            db.session.commit()
            flash('Studentų sąrašas atnaujintas!', 'success')
            return redirect(url_for('view_group', id=group.id))
        
        # Gauti visus studentus, kurie priklauso programai
        program_students = Student.query.filter_by(program_id=group.program_id).all()
        
        return render_template('groups/manage_students.html', 
                              group=group, 
                              program_students=program_students)
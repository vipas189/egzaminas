from flask import render_template, redirect, url_for, flash, request, jsonify
from models.modules import Modules
from models.schedule_model import Schedule
from models.assessments_model import Assessment
from models.exam_mode import Exam
from models.forms.module_form import ModuleForm
from models.forms.schedule_form import ScheduleForm
from models.forms.assessment_form import AssessmentForm
from models.forms.exam_form import ExamForm
from extensions import db

def home_route(app):
    # List all modules
    @app.route('/modules')
    def list_modules():
        modules = Modules.query.all()
        return render_template('modules/index.html', modules=modules)

    # Create new module
    @app.route('/modules/create', methods=['GET', 'POST'])
    def create_module():
        form = ModuleForm()
        if form.validate_on_submit():
            module = Modules(
                name=form.name.data,
                description=form.description.data,
                credits=form.credits.data,
                semester=form.semester.data,
                prerequisites=form.prerequisites.data
            )
            db.session.add(module)
            db.session.commit()
            flash('Module created successfully!', 'success')
            return redirect(url_for('view_module', id=module.id))
        return render_template('modules/create.html', form=form)

    # View module details
    @app.route('/modules/<int:id>')
    def view_module(id):
        module = Modules.query.get_or_404(id)
        schedules = Schedule.query.filter_by(module_id=id).all()
        assessments = Assessment.query.filter_by(module_id=id).all()
        exams = Exam.query.filter_by(module_id=id).all()
        
        return render_template('modules/view.html', 
                            module=module, 
                            schedules=schedules,
                            assessments=assessments,
                            exams=exams)

    # Edit module
    @app.route('/modules/<int:id>/edit', methods=['GET', 'POST'])
    def edit_module(id):
        module = Modules.query.get_or_404(id)
        form = ModuleForm(obj=module)
        
        if form.validate_on_submit():
            form.populate_obj(module)
            db.session.commit()
            flash('Module updated successfully!', 'success')
            return redirect(url_for('view_module', id=module.id))
        
        return render_template('modules/edit.html', form=form, module=module)

    # Delete module
    @app.route('/modules/<int:id>/delete', methods=['POST'])
    def delete_module(id):
        module = Modules.query.get_or_404(id)
        db.session.delete(module)
        db.session.commit()
        flash('Module deleted successfully!', 'success')
        return redirect(url_for('list_modules'))

    # Schedule management
    @app.route('/modules/<int:id>/schedules/add', methods=['GET', 'POST'])
    def add_schedule(id):
        module = Modules.query.get_or_404(id)
        form = ScheduleForm()
        
        if form.validate_on_submit():
            schedule = Schedule(
                module_id=id,
                day_of_week=form.day_of_week.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                location=form.location.data,
                lecture_type=form.lecture_type.data
            )
            db.session.add(schedule)
            db.session.commit()
            flash('Schedule added successfully!', 'success')
            return redirect(url_for('view_module', id=id))
        
        return render_template('modules/add_schedule.html', form=form, module=module)

    @app.route('/modules/<int:module_id>/schedules/<int:schedule_id>/edit', methods=['GET', 'POST'])
    def edit_schedule(module_id, schedule_id):
        module = Modules.query.get_or_404(module_id)
        schedule = Schedule.query.get_or_404(schedule_id)
        
        if schedule.module_id != module_id:
            flash('Invalid schedule for this module!', 'danger')
            return redirect(url_for('view_module', id=module_id))
        
        form = ScheduleForm(obj=schedule)
        
        if form.validate_on_submit():
            form.populate_obj(schedule)
            db.session.commit()
            flash('Schedule updated successfully!', 'success')
            return redirect(url_for('view_module', id=module_id))
        
        return render_template('modules/edit_schedule.html', form=form, module=module, schedule=schedule)

    @app.route('/modules/<int:module_id>/schedules/<int:schedule_id>/delete', methods=['POST'])
    def delete_schedule(module_id, schedule_id):
        schedule = Schedule.query.get_or_404(schedule_id)
        
        if schedule.module_id != module_id:
            flash('Invalid schedule for this module!', 'danger')
            return redirect(url_for('view_module', id=module_id))
        
        db.session.delete(schedule)
        db.session.commit()
        flash('Schedule deleted successfully!', 'success')
        return redirect(url_for('view_module', id=module_id))

    # Assessment management
    @app.route('/modules/<int:id>/assessments/add', methods=['GET', 'POST'])
    def add_assessment(id):
        module = Modules.query.get_or_404(id)
        form = AssessmentForm()
        
        if form.validate_on_submit():
            assessment = Assessment(
                module_id=id,
                title=form.title.data,
                description=form.description.data,
                due_date=form.due_date.data,
                weight=form.weight.data
            )
            db.session.add(assessment)
            db.session.commit()
            flash('Assessment added successfully!', 'success')
            return redirect(url_for('view_module', id=id))
        
        return render_template('modules/add_assessment.html', form=form, module=module)

    @app.route('/modules/<int:module_id>/assessments/<int:assessment_id>/edit', methods=['GET', 'POST'])
    def edit_assessment(module_id, assessment_id):
        module = Modules.query.get_or_404(module_id)
        assessment = Assessment.query.get_or_404(assessment_id)
        
        if assessment.module_id != module_id:
            flash('Invalid assessment for this module!', 'danger')
            return redirect(url_for('view_module', id=module_id))
        
        form = AssessmentForm(obj=assessment)
        
        if form.validate_on_submit():
            form.populate_obj(assessment)
            db.session.commit()
            flash('Assessment updated successfully!', 'success')
            return redirect(url_for('view_module', id=module_id))
        
        return render_template('modules/edit_assessment.html', form=form, module=module, assessment=assessment)

    @app.route('/modules/<int:module_id>/assessments/<int:assessment_id>/delete', methods=['POST'])
    def delete_assessment(module_id, assessment_id):
        assessment = Assessment.query.get_or_404(assessment_id)
        
        if assessment.module_id != module_id:
            flash('Invalid assessment for this module!', 'danger')
            return redirect(url_for('view_module', id=module_id))
        
        db.session.delete(assessment)
        db.session.commit()
        flash('Assessment deleted successfully!', 'success')
        return redirect(url_for('view_module', id=module_id))

    # Exam management
    @app.route('/modules/<int:id>/exams/add', methods=['GET', 'POST'])
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
                weight=form.weight.data
            )
            db.session.add(exam)
            db.session.commit()
            flash('Exam added successfully!', 'success')
            return redirect(url_for('view_module', id=id))
        
        return render_template('modules/add_exam.html', form=form, module=module)

    @app.route('/modules/<int:module_id>/exams/<int:exam_id>/edit', methods=['GET', 'POST'])
    def edit_exam(module_id, exam_id):
        module = Modules.query.get_or_404(module_id)
        exam = Exam.query.get_or_404(exam_id)
        
        if exam.module_id != module_id:
            flash('Invalid exam for this module!', 'danger')
            return redirect(url_for('view_module', id=module_id))
        
        form = ExamForm(obj=exam)
        
        if form.validate_on_submit():
            form.populate_obj(exam)
            db.session.commit()
            flash('Exam updated successfully!', 'success')
            return redirect(url_for('view_module', id=module_id))
        
        return render_template('modules/edit_exam.html', form=form, module=module, exam=exam)

    @app.route('/modules/<int:module_id>/exams/<int:exam_id>/delete', methods=['POST'])
    def delete_exam(module_id, exam_id):
        exam = Exam.query.get_or_404(exam_id)
        
        if exam.module_id != module_id:
            flash('Invalid exam for this module!', 'danger')
            return redirect(url_for('view_module', id=module_id))
        
        db.session.delete(exam)
        db.session.commit()
        flash('Exam deleted successfully!', 'success')
        return redirect(url_for('view_module', id=module_id))
        
    # Basic home page
    @app.route('/')
    def home():
        return redirect(url_for('list_modules'))
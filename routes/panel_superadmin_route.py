from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from config import Config
from services.admin_dashboard_section_services import get_users_count, get_program_count
from services.admin_crud_section_service import get_users, add_user, update_user, get_user_by_id
from models.form.admin_add_user_form import AddUserForm
from werkzeug.security import generate_password_hash
from services.program_services import program_name_to_id
from models.program import Program

def panel_superadmin_route(app):
    @app.route("/panel/superadmin")
    @login_required
    def panel_superadmin():
        # DASHBOARD/STATISTIKA
        students_count = get_users_count('student')
        lecturer_count = get_users_count('lecturer')
        admin_count = get_users_count('admin')
        program_count = get_program_count()
        # group_count = get_group_count()

        # VARTOTOJU VALDYMAS
        users_list = get_users()
    
        return render_template('panel_superadmin.html',
                               students_count=students_count,
                               lecturer_count = lecturer_count,
                               admin_count = admin_count,
                               program_count = program_count,
                            #    group_count = group_count,
                                users_list = users_list,
                                form = AddUserForm(),
                                Config=Config
                               )
    
    @app.route("/panel/superadmin/add", methods=["POST"])
    def add():
        form = AddUserForm()
        program_id = None
        if form.role.data == 'student':
            if form.program.data:
                program_id = program_name_to_id(form.program.data)
            else:
                flash("Studentui turi būti paskirta studijų programa", category= 'no_program_selected')
                return redirect(url_for('panel_superadmin'))
        add_user(
            form.name.data,
            form.last_name.data,
            form.email.data,
            generate_password_hash(form.password.data),
            form.role.data,
            program_name_to_id(form.program.data)
        )
        flash("Vartotojas buvo sėkmingai pridėtas!", category= 'user_added')
        return redirect(url_for('panel_superadmin'))
    
            
    @app.route("/panel/superadmin/edit", methods=["POST"])
    def edit():
        user = get_user_by_id()
        
        form = AddUserForm()

        
        user.name = form.name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        
        if form.password.data:
            user.password = generate_password_hash(form.password.data)
        
        user.role = form.role.data
        
        if user.role == 'student':
            if form.program.data:
                user.program = program_name_to_id(form.program.data)
            else:
                flash("Studentui turi būti paskirta studijų programa", category='no_program_selected')
                return redirect(url_for('panel_superadmin'))
        
        update_user(user)  # Function to update user in database
        flash("Vartotojo duomenys sėkmingai atnaujinti!", category='user_updated')
        return redirect(url_for('panel_superadmin'))
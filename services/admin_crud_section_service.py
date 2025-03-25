from models.users import Users
from extensions import db
from models.form.admin_add_user_form import AddUserForm
from services.program_services import program_name_to_id

def get_users():
    users = db.session.execute(db.select(Users)).scalars().all()
    return users


def add_user(name, last_name, email, password, role, program):

    new_user = Users(
        name=name,
        last_name=last_name,
        email=email,
        password=password,
        role=role,
        program_id = program

    )
    db.session.add(new_user)
    db.session.commit()

def update_user(name, last_name, email, password, role, program):
        
    user = db.session.execute(db.select(Users).filter_by(email = email)).scalar_one_or_none()
    user.name = name
    user.last_name = last_name
    user.password = password
    user.role = role
    user.program = program

    db.session.commit()

def get_user_by_id(user_id):
    user = db.session.execute(db.select(Users).filter_by(id=user_id)).scalar_one_or_none()
    return user


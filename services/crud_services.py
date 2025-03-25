from extensions import db
from services.program_to_id_services import program_to_id
from werkzeug.security import generate_password_hash
from models.users import Users


def create_user(name, last_name, email, password, role, program):
    if program == None:
        user = Users(
            name=name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password),
            role=role,
        )
        db.session.add(user)
        db.session.commit()
        return
    user = Users(
        name=name,
        last_name=last_name,
        email=email,
        password=generate_password_hash(password),
        role=role,
        program_id=program_to_id(program),
    )
    db.session.add(user)
    db.session.commit()


def read_users():
    users = db.session.execute(db.select(Users)).scalars().all()
    return users


def update_user(id, name, last_name, email, password, role, program):
    user = db.session.execute(db.select(Users).filter_by(id=id)).scalar()
    if program == None:
        user.name = name
        user.last_name = last_name
        user.email = email
        user.password = generate_password_hash(password)
        user.role = role
        user.program = None
        db.session.commit()
        return
    user.name = name
    user.last_name = last_name
    user.email = email
    user.password = generate_password_hash(password)
    user.role = role
    user.program_id = program_to_id(program)
    db.session.commit()


def remove_user(id):
    user = db.session.execute(db.select(Users).filter_by(id=id)).scalar()
    db.session.delete(user)
    db.session.commit()

from models.users import Users
from extensions import db
from models.program import Program
from models.modules import Modules

def get_users_count(role):
    users = db.session.execute(db.select(Users).filter_by(role=role)).scalars().all()
    return len(users)

def get_program_count():
    program = db.session.execute(db.select(Program)).scalars().all()
    return len(program)

def get_modules_count():
    modules = db.session.execute(db.select(Modules)).scalars().all()
    return len(modules)
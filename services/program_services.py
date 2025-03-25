from extensions import db
from models.program import Program

def program_name_to_id(name):
    program = db.session.execute(db.select(Program).filter_by(name=name)).scalar_one_or_none()
    return program.id

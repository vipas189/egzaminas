from extensions import db
from models.program import Program


def program_to_id(program_name):
    program = db.session.execute(
        db.select(Program).filter_by(name=program_name)
    ).scalar()
    return program.id

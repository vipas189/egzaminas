from extensions import db
from models.study_programs import StudyPrograms


def study_programs():
    study_program = db.session.execute(db.select(StudyPrograms)).scalars().all()
    return study_program


def study_program_name_to_id(study_program_name):
    study_program = db.session.execute(
        db.select(StudyPrograms).filter_by(name=study_program_name)
    ).scalar()
    return study_program.id

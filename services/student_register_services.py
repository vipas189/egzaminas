from extensions import db
from models.students import Students


def student_exists(email):
    student = db.session.execute(db.select(Students).filter_by(email=email)).scalar()
    return student


def student_add(name, last_name, email, password, study_program):
    # check_password_hash(hashed_password, password)
    student = Students(
        name=name,
        last_name=last_name,
        email=email,
        password=password,
        study_program=study_program,
    )
    db.session.add(student)
    db.session.commit()

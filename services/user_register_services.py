from extensions import db
from models.users import Users


def user_exists(email):
    lecturer = db.session.execute(db.select(Users).filter_by(email=email)).scalar()
    return lecturer


def lecturer_add(name, last_name, email, password):
    lecturer = Users(name=name, last_name=last_name, email=email, password=password)
    db.session.add(lecturer)
    db.session.commit()


def student_add(name, last_name, email, password, study_program):
    # check_password_hash(hashed_password, password)
    student = Users(
        name=name,
        last_name=last_name,
        email=email,
        password=password,
        study_program=study_program,
    )
    db.session.add(student)
    db.session.commit()

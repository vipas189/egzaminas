from extensions import db
from models.users import Users
from config import Config


def user_exists(email):
    lecturer = db.session.execute(db.select(Users).filter_by(email=email)).scalar()
    if email == Config.ADMIN_EMAIL:
        return True
    return lecturer


def student_add(name, last_name, email, password, study_program_id):
    # check_password_hash(hashed_password, password)
    student = Users(
        name=name,
        last_name=last_name,
        email=email,
        password=password,
        role="student",
        study_program_id=study_program_id,
    )
    db.session.add(student)
    db.session.commit()
    return student


def lecturer_add(name, last_name, email, password):
    lecturer = Users(
        name=name, last_name=last_name, email=email, password=password, role="lecturer"
    )
    db.session.add(lecturer)
    db.session.commit()
    return lecturer

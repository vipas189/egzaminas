from extensions import db
from models.students import Students


def student_exists(email):
    student = db.session.execute(db.select(Students).filter_by(email=email)).scalar()
    return student

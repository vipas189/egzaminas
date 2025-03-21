from extensions import db
from models.lecturers import Lecturers


def lecturer_exists(email):
    lecturer = db.session.execute(db.select(Lecturers).filter_by(email=email)).scalar()
    return lecturer


def lecturer_add(email, password):
    lecturer = Lecturers(email, password)
    db.session.add(lecturer)
    db.session.commit()

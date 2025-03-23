from extensions import db


class StudyPrograms(db.Model):
    __tablename__ = "study_programs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)  # e.g., P000F001
    description = db.Column(db.Text)

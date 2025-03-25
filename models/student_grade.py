from extensions import db
from datetime import datetime


class StudentGrade(db.Model):
    __tablename__ = "student_grade"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id"), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessment.id"))
    exam_id = db.Column(db.Integer, db.ForeignKey("exam.id"))
    grade = db.Column(db.Float, nullable=False)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Ryšiai
    module = db.relationship("Modules")
    assessment = db.relationship("Assessment", foreign_keys=[assessment_id])
    exam = db.relationship("Exam", foreign_keys=[exam_id])

    def __repr__(self):
        return f"<StudentGrade {self.student_id}-{self.module_id}: {self.grade}>"

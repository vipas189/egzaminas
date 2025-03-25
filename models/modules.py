from extensions import db
from datetime import datetime


class Modules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    prerequisites = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # # Relationships
    # schedules = db.relationship("Schedule", backref="module")
    # assessments = db.relationship("Assessment", backref="module")
    # exams = db.relationship("Exam", backref="module")
    # instructors = db.relationship(
    #     "Instructor", secondary="module_instructor", backref="modules"
    # # )

    # def __repr__(self):
    #     return f"<Modules {self.name}>"

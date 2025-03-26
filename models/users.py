from extensions import db
from flask_login import UserMixin
from datetime import datetime


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    profile_picture = db.Column(db.String(255), default="uploads/profile_stock.jpg")
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Security
    login_attempts = db.Column(db.Integer, default=0)
    last_failed_login = db.Column(db.DateTime)
    suspended_until = db.Column(db.DateTime)

    # ForeignKeys
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"))
    selected_modules = db.relationship(
        "Modules", secondary="student_module", backref="enrolled_students"
    )

    # Relationships
    program = db.relationship("Program", backref="users")
    grades = db.relationship(
        "StudentGrade", backref="users", cascade="all, delete-orphan"
    )

    # Ryšys su testo bandymais
    test_attempts = db.relationship(
        "TestAttempt", backref="users", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Student {self.name} {self.last_name}>"


# Tarpinė lentelė studentų ir modulių ryšiui
student_module = db.Table(
    "student_module",
    db.Column("student_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("module_id", db.Integer, db.ForeignKey("modules.id"), primary_key=True),
)


# Studentų pažymių modelis
class StudentGrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id"), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessment.id"))
    exam_id = db.Column(db.Integer, db.ForeignKey("exam.id"))
    test_id = db.Column(db.Integer, db.ForeignKey("test.id"))
    grade = db.Column(db.Float, nullable=False)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Ryšiai
    module = db.relationship("Modules")
    assessment = db.relationship("Assessment", foreign_keys=[assessment_id])
    exam = db.relationship("Exam", foreign_keys=[exam_id])
    test = db.relationship("Test", foreign_keys=[test_id])

    def __repr__(self):
        return f"<StudentGrade {self.student_id}-{self.module_id}: {self.grade}>"

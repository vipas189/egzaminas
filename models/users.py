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
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))

    # Relationships
    program = db.relationship("Program", backref="users")
    group = db.relationship("Groups", backref="users")
    grades = db.relationship(
        "StudentGrade", backref="users", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Student {self.name} {self.last_name}>"

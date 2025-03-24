from extensions import db
from datetime import datetime

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Ryšys su programa
    program = db.relationship('Program', backref='students')
    
    # Ryšys su pasirinktais moduliais (many-to-many)
    selected_modules = db.relationship('Modules', secondary='student_module', backref='enrolled_students')
    
    # Ryšys su studento pažymiais
    grades = db.relationship('StudentGrade', backref='student', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Student {self.name} {self.last_name}>'

# Tarpinė lentelė studentų ir modulių ryšiui
student_module = db.Table('student_module',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('modules.id'), primary_key=True))
    
# Studentų pažymių modelis
class StudentGrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    grade = db.Column(db.Float, nullable=False)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Ryšiai
    module = db.relationship('Modules')
    assessment = db.relationship('Assessment', foreign_keys=[assessment_id])
    exam = db.relationship('Exam', foreign_keys=[exam_id])
    
    def __repr__(self):
        return f'<StudentGrade {self.student_id}-{self.module_id}: {self.grade}>'
from extensions import db
from datetime import datetime

class StudentGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Ryšys su programa
    program = db.relationship('Program', backref='groups')
    
    # Ryšys su studentais (many-to-many)
    students = db.relationship('Student', secondary='student_group_membership', backref='groups')
    
    def __repr__(self):
        return f'<StudentGroup {self.name}>'

# Tarpinė lentelė studentų ir grupių ryšiui
student_group_membership = db.Table('student_group_membership',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('student_group.id'), primary_key=True)
)
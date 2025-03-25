from extensions import db
from datetime import datetime

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # # Ryšis su moduliais (many-to-many)
    # modules = db.relationship('Modules', secondary='program_module', backref='programs')
    
    # def __repr__(self):
    #     return f'<Program {self.name}>'
    
    # program_module = db.Table('program_module',
    #     db.Column('program_id', db.Integer, db.ForeignKey('program.id'), primary_key=True),
    #     db.Column('module_id', db.Integer, db.ForeignKey('modules.id'), primary_key=True))
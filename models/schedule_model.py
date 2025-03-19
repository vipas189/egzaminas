from extensions import db
from datetime import datetime

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100))
    lecture_type = db.Column(db.String(50), nullable=False)  # Lecture, Lab, Seminar, etc.
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Schedule {self.day_of_week} {self.start_time}-{self.end_time}>'
from extensions import db
from datetime import datetime


class StudentCalendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(
        db.String(20), nullable=False
    )  # 'schedule', 'assessment', 'exam'
    module_id = db.Column(db.Integer, db.ForeignKey("modules.id"), nullable=False)
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Ryšys su studentu
    student = db.relationship("Users", backref="calendar_events")

    # Ryšys su moduliu
    module = db.relationship("Modules")

    def __repr__(self):
        return f"<StudentCalendar {self.title} - {self.student_id}>"

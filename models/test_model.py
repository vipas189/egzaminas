from extensions import db
from datetime import datetime

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # minutes
    passing_score = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)  # Nustatyta kaip True pagal nutylėjimą
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    module = db.relationship('Modules', backref='tests')
    instructor = db.relationship('Instructor', backref='tests')
    questions = db.relationship('TestQuestion', backref='test', cascade='all, delete-orphan')
    attempts = db.relationship('TestAttempt', backref='test', cascade='all, delete-orphan')


class TestQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # 'multiple_choice', 'true_false', 'text'
    points = db.Column(db.Integer, default=1)
    
    # Relationships
    options = db.relationship('TestQuestionOption', backref='question', cascade='all, delete-orphan')


class TestQuestionOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('test_question.id'), nullable=False)
    option_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)


class TestAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    score = db.Column(db.Float)
    passed = db.Column(db.Boolean)
    
    # Relationships
    answers = db.relationship('TestAnswer', backref='attempt', cascade='all, delete-orphan')


class TestAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('test_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('test_question.id'), nullable=False)
    selected_option_id = db.Column(db.Integer, db.ForeignKey('test_question_option.id'))
    text_answer = db.Column(db.Text)
    is_correct = db.Column(db.Boolean)
    points_earned = db.Column(db.Float)
    
    # Relationships
    question = db.relationship('TestQuestion')
    selected_option = db.relationship('TestQuestionOption')
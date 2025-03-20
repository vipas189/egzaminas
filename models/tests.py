from extensions import db

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    test_name = db.Column(db.String(100), nullable=False)
    module_id = db.Column(db.Integer, nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    answer_1 = db.Column(db.String(200), nullable=False)
    answer_2 = db.Column(db.String(200), nullable=False)
    answer_3 = db.Column(db.String(200))
    answer_4 = db.Column(db.String(200))
    correct_answer = db.Column(db.String(1), nullable=False)

    test = db.relationship('Test', backref=db.backref('questions', lazy=True))
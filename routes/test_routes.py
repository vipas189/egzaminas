from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Test
from services.test_service import create_test, get_test_by_id

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_management.db'
app.config['SECRET_KEY'] = 'slaptas-raktas'

db.init_app(app)

@app.route('/tests/create', methods=['GET', 'POST'])
def create_test_route():
    if request.method == 'POST':
        title = request.form.get('title')
        module_id = request.form.get('module_id')
        user_id = request.form.get('user_id')
        questions = []

        for i in range(int(request.form.get('question_count'))):
            question_text = request.form.get(f'question_text_{i}')
            correct_answer = request.form.get(f'correct_answer_{i}')
            if question_text and correct_answer:
                questions.append({'text': question_text, 'answer': correct_answer})

        new_test = create_test(title, module_id, user_id, questions)
        if new_test:
            flash('Testas sukurtas sėkmingai!', 'success')
            return redirect(url_for('list_tests'))
        flash('Nepavyko sukurti testo.', 'danger')

    return render_template('create_test.html')

@app.route('/tests/<int:test_id>')
def view_test(test_id):
    test = get_test_by_id(test_id)
    if not test:
        flash('Testas nerastas.', 'danger')
        return redirect(url_for('list_tests'))
    return render_template('view_test.html', test=test)

@app.route('/tests')
def list_tests():
    tests = Test.query.all()
    return render_template('list_tests.html', tests=tests)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from models.test_model import Test, TestQuestion, TestQuestionOption, TestAttempt, TestAnswer
from models.modules import Modules
from models.instructor_model import Instructor
from models.students import Student, StudentGrade
from models.forms.test_form import TestForm, TestQuestionForm
from extensions import db
from datetime import datetime, timedelta

def test_routes(app):
    @app.route('/tests')
    def list_tests():
        tests = Test.query.all()
        return render_template('tests/index.html', tests=tests)

    @app.route('/instructors/<int:instructor_id>/tests')
    def instructor_tests(instructor_id):
        instructor = Instructor.query.get_or_404(instructor_id)
        tests = Test.query.filter_by(instructor_id=instructor_id).all()
        return render_template('tests/instructor_tests.html', instructor=instructor, tests=tests)

    @app.route('/instructors/<int:instructor_id>/tests/create', methods=['GET', 'POST'])
    def create_test(instructor_id):
        instructor = Instructor.query.get_or_404(instructor_id)
        form = TestForm()
        
        # Užpildyti modulių pasirinkimą (tik tie moduliai, kuriuos dėsto šis dėstytojas)
        form.module_id.choices = [(m.id, m.name) for m in instructor.modules]
        
        if form.validate_on_submit():
            test = Test(
                title=form.title.data,
                description=form.description.data,
                module_id=form.module_id.data,
                instructor_id=instructor_id,
                duration=form.duration.data,
                passing_score=form.passing_score.data,
                weight=form.weight.data
            )
            db.session.add(test)
            db.session.commit()
            flash('Testas sukurtas sėkmingai!', 'success')
            return redirect(url_for('edit_test_questions', test_id=test.id))
            
        return render_template('tests/create.html', form=form, instructor=instructor)

    @app.route('/tests/<int:test_id>/questions', methods=['GET', 'POST'])
    def edit_test_questions(test_id):
        test = Test.query.get_or_404(test_id)
        
        if request.method == 'POST':
            data = request.json
            
            # Ištrinti esamus klausimus ir atsakymus
            for question in test.questions:
                db.session.delete(question)
            
            # Pridėti naujus klausimus ir atsakymus
            for q_data in data.get('questions', []):
                question = TestQuestion(
                    test_id=test.id,
                    question_text=q_data.get('text'),
                    question_type=q_data.get('type'),
                    points=q_data.get('points', 1)
                )
                db.session.add(question)
                db.session.flush()  # Gauti klausimo ID
                
                for o_data in q_data.get('options', []):
                    option = TestQuestionOption(
                        question_id=question.id,
                        option_text=o_data.get('text'),
                        is_correct=o_data.get('is_correct', False)
                    )
                    db.session.add(option)
            
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Klausimai išsaugoti sėkmingai'})
        
        questions = TestQuestion.query.filter_by(test_id=test.id).all()
        return render_template('tests/edit_questions.html', test=test, questions=questions)

    @app.route('/tests/<int:test_id>/preview')
    def preview_test(test_id):
        test = Test.query.get_or_404(test_id)
        questions = TestQuestion.query.filter_by(test_id=test.id).all()
        return render_template('tests/preview.html', test=test, questions=questions)

    @app.route('/students/<int:student_id>/tests')
    def student_tests(student_id):
        student = Student.query.get_or_404(student_id)
        
        # Gauti modulius, kuriuos yra pasirinkęs studentas
        modules = student.selected_modules
        
        # Gauti testus, kurie yra priskirti šiems moduliams
        available_tests = []
        for module in modules:
            module_tests = Test.query.filter_by(module_id=module.id, is_active=True).all()
            for test in module_tests:
                # Patikrinti, ar studentas jau atliko šį testą
                attempt = TestAttempt.query.filter_by(test_id=test.id, student_id=student.id).first()
                available_tests.append({
                    'test': test,
                    'module': module,
                    'completed': attempt is not None,
                    'score': attempt.score if attempt else None,
                    'passed': attempt.passed if attempt else None,
                    'attempt': attempt  # Pridėta trūkstama informacija apie bandymą
                })
                
        return render_template('tests/student_tests.html', student=student, available_tests=available_tests)

    @app.route('/students/<int:student_id>/tests/<int:test_id>/start', methods=['GET', 'POST'])
    def start_test(student_id, test_id):
        student = Student.query.get_or_404(student_id)
        test = Test.query.get_or_404(test_id)
        
        # Patikrinti, ar studentas jau atliko šį testą
        existing_attempt = TestAttempt.query.filter_by(test_id=test.id, student_id=student.id).first()
        if existing_attempt:
            flash('Jūs jau atliekate šį testą. Tęskite.', 'warning')
            return redirect(url_for('take_test', student_id=student.id, test_id=test.id, attempt_id=existing_attempt.id))
        
        # Sukurti naują bandymą
        attempt = TestAttempt(
            test_id=test.id,
            student_id=student.id,
            start_time=datetime.now()
        )
        db.session.add(attempt)
        db.session.commit()
        
        return redirect(url_for('take_test', student_id=student.id, test_id=test.id, attempt_id=attempt.id))

    @app.route('/students/<int:student_id>/tests/<int:test_id>/attempt/<int:attempt_id>', methods=['GET', 'POST'])
    def take_test(student_id, test_id, attempt_id):
        student = Student.query.get_or_404(student_id)
        test = Test.query.get_or_404(test_id)
        attempt = TestAttempt.query.get_or_404(attempt_id)
        
        # Patikrinti, ar bandymas priklauso šiam studentui
        if attempt.student_id != student.id:
            flash('Prieigos klaida!', 'danger')
            return redirect(url_for('student_tests', student_id=student.id))
        
        # Patikrinti, ar testas dar nebaigtas
        if attempt.end_time:
            flash('Šis testas jau užbaigtas!', 'info')
            return redirect(url_for('view_test_results', student_id=student.id, test_id=test.id, attempt_id=attempt.id))
        
        # Patikrinti, ar nepasibaigė laikas
        time_limit = attempt.start_time + timedelta(minutes=test.duration)
        time_remaining = (time_limit - datetime.now()).total_seconds()
        
        if time_remaining <= 0:
            # Automatiškai užbaigti testą, jei baigėsi laikas
            return grade_test(attempt)
            
        if request.method == 'POST':
            # Išsaugoti atsakymus
            for key, value in request.form.items():
                if key.startswith('question_'):
                    question_id = int(key.split('_')[1])
                    question = TestQuestion.query.get(question_id)
                    
                    # Pašalinti senus atsakymus
                    TestAnswer.query.filter_by(attempt_id=attempt.id, question_id=question_id).delete()
                    
                    # Sukurti naują atsakymą pagal klausimo tipą
                    if question.question_type == 'multiple_choice':
                        selected_option_id = int(value) if value else None
                        if selected_option_id:
                            option = TestQuestionOption.query.get(selected_option_id)
                            answer = TestAnswer(
                                attempt_id=attempt.id,
                                question_id=question_id,
                                selected_option_id=selected_option_id,
                                is_correct=option.is_correct,
                                points_earned=question.points if option.is_correct else 0
                            )
                            db.session.add(answer)
                    
                    elif question.question_type == 'true_false':
                        selected_option_id = int(value) if value else None
                        if selected_option_id:
                            option = TestQuestionOption.query.get(selected_option_id)
                            answer = TestAnswer(
                                attempt_id=attempt.id,
                                question_id=question_id,
                                selected_option_id=selected_option_id,
                                is_correct=option.is_correct,
                                points_earned=question.points if option.is_correct else 0
                            )
                            db.session.add(answer)
                    
                    elif question.question_type == 'text':
                        # Tekstiniai atsakymai bus vertinami dėstytojo
                        answer = TestAnswer(
                            attempt_id=attempt.id,
                            question_id=question_id,
                            text_answer=value,
                            is_correct=None,
                            points_earned=None
                        )
                        db.session.add(answer)
            
            db.session.commit()
            
            # Patikrinti, ar reikia baigti testą
            if 'finish_test' in request.form:
                return grade_test(attempt)
                
            flash('Atsakymai išsaugoti!', 'success')
            
        questions = TestQuestion.query.filter_by(test_id=test.id).all()
        answers = TestAnswer.query.filter_by(attempt_id=attempt.id).all()
        
        # Surinkti esamus atsakymus į žodyną
        user_answers = {}
        for answer in answers:
            if answer.selected_option_id:
                user_answers[answer.question_id] = answer.selected_option_id
            elif answer.text_answer:
                user_answers[answer.question_id] = answer.text_answer
        
        return render_template('tests/take_test.html', 
                              student=student, 
                              test=test, 
                              attempt=attempt,
                              questions=questions,
                              user_answers=user_answers,
                              time_remaining=time_remaining)

    def grade_test(attempt):
        test = Test.query.get(attempt.test_id)
        student = Student.query.get(attempt.student_id)
        
        # Užbaigti bandymą
        attempt.end_time = datetime.now()
        
        # Apskaičiuoti rezultatą
        questions = TestQuestion.query.filter_by(test_id=test.id).all()
        answers = TestAnswer.query.filter_by(attempt_id=attempt.id).all()
        
        total_points = sum(q.points for q in questions)
        earned_points = sum(a.points_earned or 0 for a in answers if a.points_earned is not None)
        
        # Apskaičiuoti procentinį rezultatą
        attempt.score = (earned_points / total_points * 100) if total_points > 0 else 0
        
        # Nustatyti, ar išlaikyta
        attempt.passed = attempt.score >= test.passing_score
        
        # Jei išlaikyta, pridėti pažymį
        if attempt.passed and test.weight > 0:
            # Patikrinti, ar jau yra įrašytas pažymys
            existing_grade = StudentGrade.query.filter_by(
                student_id=student.id,
                module_id=test.module_id,
                test_id=test.id
            ).first()
            
            if existing_grade:
                existing_grade.grade = attempt.score
                existing_grade.updated_at = datetime.now()
            else:
                # Sukurti naują pažymį
                grade = StudentGrade(
                    student_id=student.id,
                    module_id=test.module_id,
                    test_id=test.id,
                    grade=attempt.score,
                    feedback=f'Testas „{test.title}" išlaikytas su {attempt.score:.2f}% rezultatu.'
                )
                db.session.add(grade)
        
        db.session.commit()
        
        flash(f'Testas baigtas! Jūsų rezultatas: {attempt.score:.2f}%', 'info')
        return redirect(url_for('view_test_results', 
                               student_id=student.id, 
                               test_id=test.id, 
                               attempt_id=attempt.id))

    @app.route('/students/<int:student_id>/tests/<int:test_id>/attempt/<int:attempt_id>/results')
    def view_test_results(student_id, test_id, attempt_id):
        student = Student.query.get_or_404(student_id)
        test = Test.query.get_or_404(test_id)
        attempt = TestAttempt.query.get_or_404(attempt_id)
        
        # Patikrinti, ar bandymas priklauso šiam studentui
        if attempt.student_id != student.id:
            flash('Prieigos klaida!', 'danger')
            return redirect(url_for('student_tests', student_id=student.id))
        
        # Gauti klausimus ir atsakymus
        questions = TestQuestion.query.filter_by(test_id=test.id).all()
        answers = TestAnswer.query.filter_by(attempt_id=attempt.id).all()
        
        # Surinkti duomenis apie kiekvieną klausimą ir atsakymą
        results = []
        for question in questions:
            answer = next((a for a in answers if a.question_id == question.id), None)
            
            if answer:
                if question.question_type in ['multiple_choice', 'true_false']:
                    selected_option = TestQuestionOption.query.get(answer.selected_option_id) if answer.selected_option_id else None
                    
                    result = {
                        'question': question,
                        'selected_option': selected_option,
                        'is_correct': answer.is_correct,
                        'points_earned': answer.points_earned,
                        'max_points': question.points
                    }
                else:  # text question
                    result = {
                        'question': question,
                        'text_answer': answer.text_answer,
                        'points_earned': answer.points_earned,
                        'max_points': question.points
                    }
            else:
                # Neatsakytas klausimas
                result = {
                    'question': question,
                    'selected_option': None,
                    'text_answer': None,
                    'is_correct': False,
                    'points_earned': 0,
                    'max_points': question.points
                }
                
            results.append(result)
        
        return render_template('tests/results.html', 
                              student=student, 
                              test=test, 
                              attempt=attempt,
                              results=results)

    @app.route('/instructors/<int:instructor_id>/tests/<int:test_id>/review')
    def review_test_attempts(instructor_id, test_id):
        instructor = Instructor.query.get_or_404(instructor_id)
        test = Test.query.get_or_404(test_id)
        
        # Patikrinti, ar testas priklauso šiam dėstytojui
        if test.instructor_id != instructor.id:
            flash('Prieigos klaida!', 'danger')
            return redirect(url_for('instructor_tests', instructor_id=instructor.id))
        
        # Gauti visus bandymus
        attempts = TestAttempt.query.filter_by(test_id=test.id).all()
        
        # Surinkti informaciją apie kiekvieną bandymą
        attempt_info = []
        for attempt in attempts:
            student = Student.query.get(attempt.student_id)
            
            info = {
                'attempt': attempt,
                'student': student,
                'duration': (attempt.end_time - attempt.start_time).total_seconds() / 60 if attempt.end_time else None
            }
            
            attempt_info.append(info)
        
        return render_template('tests/review_attempts.html', 
                              instructor=instructor, 
                              test=test, 
                              attempts=attempt_info)

    @app.route('/instructors/<int:instructor_id>/tests/<int:test_id>/attempt/<int:attempt_id>/review', methods=['GET', 'POST'])
    def review_student_attempt(instructor_id, test_id, attempt_id):
        instructor = Instructor.query.get_or_404(instructor_id)
        test = Test.query.get_or_404(test_id)
        attempt = TestAttempt.query.get_or_404(attempt_id)
        
        # Patikrinti, ar testas priklauso šiam dėstytojui
        if test.instructor_id != instructor.id:
            flash('Prieigos klaida!', 'danger')
            return redirect(url_for('instructor_tests', instructor_id=instructor.id))
        
        student = Student.query.get(attempt.student_id)
        
        if request.method == 'POST':
            # Atnaujinti vertinimus tekstiniams klausimams
            for key, value in request.form.items():
                if key.startswith('grade_'):
                    answer_id = int(key.split('_')[1])
                    answer = TestAnswer.query.get(answer_id)
                    
                    if answer and answer.attempt_id == attempt.id:
                        points = float(value) if value else 0
                        question = TestQuestion.query.get(answer.question_id)
                        
                        answer.points_earned = min(points, question.points)
                        answer.is_correct = points > 0
            
            # Perskaičiuoti bendrą rezultatą
            questions = TestQuestion.query.filter_by(test_id=test.id).all()
            answers = TestAnswer.query.filter_by(attempt_id=attempt.id).all()
            
            total_points = sum(q.points for q in questions)
            earned_points = sum(a.points_earned or 0 for a in answers)
            
            attempt.score = (earned_points / total_points * 100) if total_points > 0 else 0
            attempt.passed = attempt.score >= test.passing_score
            
            # Atnaujinti pažymį, jei yra
            grade = StudentGrade.query.filter_by(
                student_id=student.id,
                module_id=test.module_id,
                test_id=test.id
            ).first()
            
            if grade:
                grade.grade = attempt.score
                grade.updated_at = datetime.now()
            
            db.session.commit()
            flash('Vertinimas išsaugotas!', 'success')
        
        # Gauti klausimus ir atsakymus
        questions = TestQuestion.query.filter_by(test_id=test.id).all()
        answers = TestAnswer.query.filter_by(attempt_id=attempt.id).all()
        
        # Surinkti duomenis apie kiekvieną klausimą ir atsakymą
        results = []
        for question in questions:
            answer = next((a for a in answers if a.question_id == question.id), None)
            
            if answer:
                if question.question_type in ['multiple_choice', 'true_false']:
                    selected_option = TestQuestionOption.query.get(answer.selected_option_id) if answer.selected_option_id else None
                    correct_options = TestQuestionOption.query.filter_by(question_id=question.id, is_correct=True).all()
                    
                    result = {
                        'question': question,
                        'selected_option': selected_option,
                        'correct_options': correct_options,
                        'answer': answer
                    }
                else:  # text question
                    result = {
                        'question': question,
                        'text_answer': answer.text_answer,
                        'answer': answer
                    }
            else:
                # Neatsakytas klausimas
                result = {
                    'question': question,
                    'selected_option': None,
                    'text_answer': None,
                    'answer': None
                }
                
            results.append(result)
        
        return render_template('tests/review_student_attempt.html', 
                              instructor=instructor, 
                              test=test, 
                              attempt=attempt,
                              student=student,
                              results=results)
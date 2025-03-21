from models import db, Test, Question

def create_test(title, module_id, user_id, questions):
    try:
        new_test = Test(title=title, module_id=module_id, created_by=user_id)
        for q in questions:
            new_test.questions.append(Question(
                question_text=q['text'],
                correct_answer=q['answer']
            ))
        db.session.add(new_test)
        db.session.commit()
        return new_test
    except Exception as e:
        db.session.rollback()
        print(f"Klaida kuriant testą: {e}")
        return None

def get_test_by_id(test_id):
    return Test.query.get(test_id)

def delete_test(test_id):
    try:
        test = get_test_by_id(test_id)
        if test:
            db.session.delete(test)
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Klaida trinant testą: {e}")
        return False
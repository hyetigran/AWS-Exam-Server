from db import db


class ExamModel(db.Model):
    __tablename__ = 'exams'

    id = db.Column(db.Integer, primary_key=True)
    exam_number = db.Column(db.String)
    exam_type = db.Column(db.String)
    correct = db.Column(db.Integer)
    current_question = db.Column(db.Integer)
    time = db.Column(db.String)
    is_paused = db.Column(db.Integer)
    is_finished = db.Column(db.Integer)

    questions = db.relationship('QuestionModel', lazy='dynamic')

    def __init__(self, exam_number, exam_type, correct, current_question, time, is_paused, is_finished, questions):
        self.exam_number = exam_number
        self.exam_type = exam_type
        self.correct = correct
        self.current_question = current_question
        self.time = time
        self.is_paused = is_paused
        self.is_finished = is_finished

    def json(self):
        return {
            'exam_number': self.exam_number,
            'exam_type': self.exam_type,
            'correct': self.correct,
            'current_question': self.current_question,
            'time': self.time,
            'is_paused': self.is_paused,
            'is_finished': self.is_finished,
            'questions': [question.json() for question in self.questions.all()]
        }

    def limited_json(self):
        return {
            'id': self.id,
            'exam_number': self.exam_number,
            'exam_type': self.exam_type,
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

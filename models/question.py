from db import db


class QuestionModel(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    explanation = db.Column(db.Text)
    is_multiple_choice = db.Column(db.Integer)
    status = db.Column(db.Integer)

    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    exam = db.relationship('ExamModel')
    answers = db.relationship('AnswerModel', lazy='dynamic')

    def __init__(self, question, explanation, is_multiple_choice, status, exam_id):
        self.question = question
        self.explanation = explanation
        self.is_multiple_choice = is_multiple_choice
        self.status = status
        self.exam_id = exam_id

    def json(self):
        return {
            'id': self.id,
            'question': self.question,
            'explanation': self.explanation,
            'is_multiple_choice': self.is_multiple_choice,
            'status': self.status,
            'answers': [answer.json() for answer in self.answers.all()]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

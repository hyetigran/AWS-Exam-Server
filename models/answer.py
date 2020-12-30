from db import db


class AnswerModel(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String)
    is_selected = db.Column(db.Integer)
    is_correct = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    question = db.relationship('QuestionModel')

    def __init__(self, question_id, choice, is_selected, is_correct):
        self.choice = choice
        self.is_selected = is_selected
        self.is_correct = is_correct
        self.question_id = question_id

    def json(self):
        return {
            'question_id': self.question_id,
            'answer_id': self.id,
            'choice': self.choice,
            'is_selected': self.is_selected,
            'is_correct': self.is_correct,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

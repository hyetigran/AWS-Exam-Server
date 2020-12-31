from models.exam import ExamModel
from models.question import QuestionModel
from models.answer import AnswerModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Exam(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('exam_number', type=str, required=True)
    parser.add_argument('exam_type', type=str, required=True)
    parser.add_argument('correct', type=int, required=True)
    parser.add_argument('current_question', type=int, required=True)
    parser.add_argument('time', type=str, required=True)
    parser.add_argument('is_paused', type=int, required=True)
    parser.add_argument('is_finished', type=int, required=True)
    parser.add_argument('questions', type=dict, required=True)

    def get(self, gid):
        exam = ExamModel.find_by_id(gid)
        if exam:
            return exam.json()
        return {"message": "Exam not found"}, 404

    @jwt_required()
    def post(self, gid):
        # endpoint for site admin only
        data = Exam.parser.parse_args()
        exam_number, exam_type, correct, current_question, time, is_paused, is_finished, questions = data.values()
        exam = ExamModel(exam_number, exam_type, correct,
                         current_question, time, is_paused, is_finished, questions)
        try:
            exam.save_to_db()
            for question in questions.values():
                status, question, explanation, is_multiple_choice, answers = question.values()
                new_question = QuestionModel(
                    question, explanation, is_multiple_choice, status, exam.id)
                new_question.save_to_db()
                for answer in answers.values():
                    choice, is_selected, is_correct = answer.values()
                    new_answer = AnswerModel(
                        new_question.id, choice, is_selected, is_correct)
                    new_answer.save_to_db()
        except:
            return {"message": "Error occured"}, 500
        return exam.json(), 201

    @jwt_required()
    def delete(self, gid):
        exam = ExamModel.find_by_id(gid)
        if exam:
            exam.delete_from_db()

        return {"message": "Exam deleted"}


class ExamList(Resource):
    def get(self):
        return {'exams': [exam.limited_json() for exam in ExamModel.query.all()]}

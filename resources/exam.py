from models.exam import ExamModel
from flask_restful import Resource, reqparse
import sys


class Exam(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('exam_number', type=str, required=True)
    parser.add_argument('exam_type', type=str, required=True)
    parser.add_argument('correct', type=int, required=True)
    parser.add_argument('current_question', type=int, required=True)
    parser.add_argument('time', type=str, required=True)
    parser.add_argument('is_paused', type=int, required=True)
    parser.add_argument('is_finished', type=int, required=True)

    def get(self, gid):
        exam = ExamModel.find_by_id(gid)
        if exam:
            return exam.json()
        return {"message": "Exam not found"}, 404

    def post(self, gid):
        data = Exam.parser.parse_args()
        # print(data, file=sys.stderr)
        exam = ExamModel(**data)
        try:
            exam.save_to_db()
        except:
            return {"message": "Error occured"}, 500
        return exam.json(), 201


class ExamList(Resource):
    def get(self):
        return {'exams': [exam.limited_json() for exam in ExamModel.query.all()]}

from models.question import QuestionModel
from flask_restful import Resource, reqparse
import sys


class Question(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('question', type=str, required=True)
    parser.add_argument('explanation', type=str, required=True)
    parser.add_argument('is_multiple_choice', type=int, required=True)
    parser.add_argument('status', type=int, required=True)
    parser.add_argument('exam_id', type=int, required=True)

    # Disabled
    # def post(self, gid):
    #     data = Question.parser.parse_args()
    #     # print(data, file=sys.stderr)
    #     question = QuestionModel(**data)
    #     try:
    #         question.save_to_db()
    #     except:
    #         return {"message": "Error occured"}, 500
    #     return question.json(), 201

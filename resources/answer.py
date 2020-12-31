from models.answer import AnswerModel
from flask_restful import Resource, reqparse


class Answer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('choice', type=str, required=True)
    parser.add_argument('is_selected', type=int, required=True)
    parser.add_argument('is_correct', type=int, required=True)
    parser.add_argument('question_id', type=int, required=True)

    # Disabled
    # def post(self, gid):
    #     data = Answer.parser.parse_args()
    #     # print(data, file=sys.stderr)
    #     answer = AnswerModel(**data)
    #     try:
    #         answer.save_to_db()
    #     except:
    #         return {"message": "Error occured"}, 500
    #     return answer.json(), 201

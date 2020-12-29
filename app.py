import os

from flask import Flask
from flask_restful import Resource, Api, reqparse
from db import db

from resources.exam import Exam, ExamList
from resources.question import Question
from resources.answer import Answer

app = Flask(__name__)
# app.config['SQALCHEMY_DATABASE_URI'] = os.environ.get(
#     'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
api.add_resource(Exam, '/exam/<string:gid>')
api.add_resource(ExamList, '/exams')

# Disabled endpoints
# api.add_resource(Question, '/question/<string:gid>')
# api.add_resource(Answer, '/answer/<string:gid>')

# if __name__ == '__main__':
#     from db import db
#     db.init_app(app)

#     if app.config['DEBUG']:
#         @app.before_first_request
#         def create_tables():
#             db.create_all()

#     app.run(port=5000)

# Development Env


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)  # important to mention debug=True

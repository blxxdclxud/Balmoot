from flask import jsonify
from flask_restful import reqparse, abort, Resource, Api

from data import db_session
from data.quiz_db import Quiz

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('user_id', required=True, type=int)


def abort_if_quiz_not_found(quiz_id):
    session = db_session.create_session()
    quiz = session.query(Quiz).get(quiz_id)
    if not quiz:
        abort(404, message=f"Quiz {quiz_id} not found")


class QuizResource(Resource):
    def get(self, quiz_id):
        abort_if_quiz_not_found(quiz_id)
        session = db_session.create_session()
        quiz = session.query(Quiz).get(quiz_id)
        return jsonify({'quiz': quiz.to_dict(
            only=('title', 'questions', 'user_id'))})

    def delete(self, quiz_id):
        abort_if_quiz_not_found(quiz_id)
        session = db_session.create_session()
        quiz = session.query(Quiz).get(quiz_id)
        session.delete(quiz)
        session.commit()
        return jsonify({'success': 'OK'})


class QuizListResource(Resource):
    def get(self):
        session = db_session.create_session()
        quiz = session.query(Quiz).all()
        return jsonify({'quiz': [item.to_dict(
            only=('title', 'questions', 'user_id')) for item in quiz]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        quiz = Quiz(
            title=args['title'],
            questions=args['content'],
            user_id=args['user_id']
        )
        session.add(quiz)
        session.commit()
        return jsonify({'success': 'OK'})

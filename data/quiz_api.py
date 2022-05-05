from json import loads

import flask
from flask import jsonify, abort
from requests import get

from . import db_session
from .CONSTANTS import *
from .quiz_db import Quiz

blueprint = flask.Blueprint(
    'quiz_api',
    __name__,
    template_folder='templates'
)


def get_translated_text(text, language):
    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
    params = {"langpair": f"ru|{LANGUAGES[language]}", "q": None, "mt": "1",
              "onlyprivate": "0", "de": "a@b.c"}
    headers = {
        'x-rapidapi-key': "1e969770a5msh5896a54cd19e719p155db8jsnf0d1e659764f",
        'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
    }

    params["q"] = text
    response = get(url, headers=headers, params=params)
    if not response:
        abort(404, message=f"Something's wrong. Please try later.")
        return
    json_response = response.json()
    return json_response["responseData"]["translatedText"]


@blueprint.route('/api/quiz/<int:quiz_id>/translate/<string:language>/',
                 methods=['GET'])
def translate_quiz(quiz_id, language):
    try:
        db_sess = db_session.create_session()
        quiz = db_sess.query(Quiz).filter(Quiz.id == quiz_id).first()
        json_questions = loads(quiz.questions)

        result = []

        for idx in range(len(json_questions)):
            translated_text = get_translated_text(json_questions[idx][0],
                                                  language)
            result.append([translated_text, []])
            for answer in json_questions[idx][-1]:
                translated_text = get_translated_text(answer, language)
                result[idx][-1].append([translated_text])

        return jsonify(result)
    except:
        abort(404)


@blueprint.route(
    '/api/quiz/<int:quiz_id>/translate/<string:language>/<int:question_id>',
    methods=['GET'])
def translate_question(quiz_id, language, question_id):
    try:
        db_sess = db_session.create_session()
        quiz = db_sess.query(Quiz).filter(Quiz.id == quiz_id).first()
        json_questions = loads(quiz.questions)
        current_question = json_questions[question_id]

        result = []

        translated_text = get_translated_text(current_question[0], language)
        result.append([translated_text])
        for answer in current_question[-1]:
            translated_text = get_translated_text(answer, language)
            result[-1].append([translated_text])

        return jsonify(result)
    except:
        abort(404)

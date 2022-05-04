import flask
from flask import jsonify, request
from flask_login import login_user

from . import db_session
from .user_db import User

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users/<int:start>/<int:end>', methods=['GET'])
def get_user_range(start, end):
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id >= start).filter(
        User.id < end).all()
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(only=(
                'id', 'first_name', 'last_name', 'username', 'email'))
        }
    )

import flask
from flask import jsonify, request
from flask_login import login_user

from . import db_session
from .user_db import User

blueprint = flask.Blueprint(
    'users_api',
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


@blueprint.route('/api/users/<int:pk>/', methods=['GET'])
def get_user(pk):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(pk)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=(
                'id', 'first_name', 'last_name', 'username', 'email'))
        }
    )


@blueprint.route('/api/users/login/<str:login>/<str:password>',
                 methods=['GET'])
def user_logining_get(login, password):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == login).first()
    if not user:
        user = db_sess.query(User).filter(User.email == login).first()
    if not user:
        return jsonify({'error': 'Not found'})
    if user and user.check_password(password):
        login_user(user)
    else:
        return jsonify({'error': 'Not correct password'})
    return jsonify(
        {
            'message': 'success'
        }
    )


@blueprint.route('/api/users/login', methods=['POST'])
def user_logining_post():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['login', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(
        User.username == request.json['login']).first()
    if not user:
        user = db_sess.query(User).filter(
            User.email == request.json['login']).first()
    if not user:
        return jsonify({'error': 'Not found'})
    if user and user.check_password(request.json['password']):
        login_user(user)
    else:
        return jsonify({'error': 'Not correct password'})
    return jsonify(
        {
            'message': 'success'
        }
    )


@blueprint.route('/api/users/<int:pk>', methods=['DELETE'])
def user_delete(pk):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(pk)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'message': 'success'})

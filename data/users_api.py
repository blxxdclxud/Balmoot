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


@blueprint.route(
    '/api/users/register/<str:username>/<str:email>/<str:password>'
    '/<str:password2>/<str:first_name>/<str:last_name>', methods=['GET'])
def user_creating_get(username, email, password, password2, first_name,
                      last_name):
    if password != password2:
        return jsonify({'error': 'passwords do not match'})
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == email).first():
        return jsonify({'error': 'This email is busy'})
    if db_sess.query(User).filter(User.username == username).first():
        return jsonify({'error': 'This username is busy'})
    user = User(
        first_name=first_name,
        email=email,
        last_name=last_name,
        username=username,
    )
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()
    return jsonify(
        {
            'message': 'success'
        }
    )


@blueprint.route('/api/users/create', methods=['POST'])
def user_creating_post():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['username', 'email', 'password', 'password2',
                  'first_name', 'last_name']):
        return jsonify({'error': 'Bad request'})
    if request.json['password'] != request.json['password2']:
        return jsonify({'error': 'passwords do not match'})
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == request.json['email']).first():
        return jsonify({'error': 'This email is busy'})
    if db_sess.query(User).filter(
            User.username == request.json['username']).first():
        return jsonify({'error': 'This username is busy'})
    user = User(
        first_name=request.json['first_name'],
        email=request.json['email'],
        last_name=request.json['last_name'],
        username=request.json['username'],
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify(
        {
            'user': user.to_dict(only=(
                'id', 'first_name', 'last_name', 'username', 'email'))
        }
    )


@blueprint.route(
    'api/users/edit/<int:pk>/<str:username>/<str:email>/<str:password>/'
    '<str:password2>/<str:first_name>/<str:last_name>',
    methods=['GET'])
def user_edit_get(pk, username, email, password, password2, first_name,
                  last_name):
    if password != '0' and password != password2:
        return jsonify({'error': 'passwords do not match'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(pk)
    if not user:
        return jsonify({'error': 'Not found'})
    if db_sess.query(User).filter(User.email == email).first():
        return jsonify({'error': 'This email is busy'})
    elif email != '0':
        user.email = email
    if db_sess.query(User).filter(User.username == username).first():
        return jsonify({'error': 'This username is busy'})
    elif username != '0':
        user.username = username
    if first_name != '0':
        user.first_name = first_name
    if last_name != '0':
        user.last_name = last_name
    if password != '0':
        user.set_password(password)
    db_sess.commit()
    return jsonify(
        {
            'message': 'success'
        }
    )


@blueprint.route('api/users/edit', methods=['POST'])
def user_edit_post():
    if not request.json:
        return jsonify({'error': 'Empty request'})

    if request.json['password'] != '0' and request.json['password'] != \
            request.json['password2']:
        return jsonify({'error': 'passwords do not match'})

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(request.json['pk'])

    if not user:
        return jsonify({'error': 'Not found'})

    email = request.json.get('email', False)
    if email and db_sess.query(User).filter(User.email == email).first():
        return jsonify({'error': 'This email is busy'})
    elif email:
        user.email = email
    username = request.json.get('username', False)
    if username and db_sess.query(User).filter(User.username == username).first():
        return jsonify({'error': 'This username is busy'})
    elif username:
        user.username = username

    user.first_name = request.json.get('first_name', user.first_name)
    user.last_name = request.json.get('last_name', user.last_name)
    if request.json.get('password', False):
        user.set_password(request.json['password'])
    db_sess.commit()
    return jsonify(
        {
            'message': 'success'
        }
    )

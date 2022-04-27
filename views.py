from flask import Flask, app, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.forms import LoginForm, RegisterForm
from data.user_db import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuPer-UltrA_seKretNiy_kluCH'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def main_page():
    context = {
        'title': 'Main page',
    }
    return render_template('main_pages/main_page.html', **context)


@login_manager.user_loader
def load_user(pk):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(pk)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    context = {
        'form': form,
        'title': 'Login',
    }
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.username_or_email == form.username_or_email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        context['message'] = "Неправильный логин или пароль"
        return render_template('auth/login.html', **context)
    return render_template('auth/login.html', **context)


@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    context = {
        'form': form,
        'title': 'Register',
    }
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            context['message'] = "Пароли не совпадают"
            return render_template('auth/register.html', **context)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            context['message'] = "Такой пользователь уже есть"
            return render_template('auth/register.html', **context)
        user = User(
            first_name=form.first_name.data,
            email=form.email.data,
            last_name=form.last_name.data,
            username=form.username.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('auth/register.html', **context)


@app.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/quizzes/')
def quizzes_list():
    context = {
        'title': 'List of Quizzes',
    }
    return render_template('quizzes/quizzes_lis.html', **context)


@app.route('/quizzes/<int:pk>/')  # primary key (Первичный ключ)
def quiz_info(pk):
    context = {
        'title': 'QUIZ_NAME',  # Replace with the name of quiz
    }
    return render_template('quizzes/quiz_info.html', **context)


@app.route('/quizzes/<int:pk>/delete')
def quiz_delete(pk):
    context = {
        'title': 'Quiz_delete'
    }
    return render_template('quizzes/quiz_delete.html', **context)


@app.route('/quizzes/<int:pk>/edit')
def quiz_edit(pk):
    context = {
        'title': 'QUIZ_NAME + _edit'  # Replace title
    }
    render_template('quizzes/quiz_edit.html', **context)


@app.route('/quizzes/<int:pk>/passing/<int:question_num>')
def quiz_pass(pk, question_num):
    context = {
        'title': 'QUESTION_NAME'  # Replace title
    }
    render_template('quizzes/quiz_pass.html', **context)


def main():
    app.debug = True
    app.run(port=8080, host='127.0.0.1')

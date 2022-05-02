from json import dumps, loads

from flask import Flask, app, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from flask_restful import Api

from data import db_session, quiz_resources
from data.forms import LoginForm, RegisterForm, EditForm, QuizCreateForm, \
    QuizEditForm
from data.quiz_db import Quiz
from data.user_db import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuPer-UltrA|m366a}_seKretNiy_kluCH'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

api.add_resource(quiz_resources.QuizListResource, '/api/v2/news')
api.add_resource(quiz_resources.QuizResource, '/api/v2/news/<int:news_id>')


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


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    context = {
        'form': form,
        'title': 'Login',
    }
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.username == form.username_or_email.data).first()
        if not user:
            user = db_sess.query(User).filter(
                User.email == form.username_or_email.data).first()
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
        return redirect('/auth/login')
    return render_template('auth/register.html', **context)


@app.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/auth/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditForm()
    context = {
        'title': str(current_user.username),
        'form': form,
    }
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()

        if form.password.data != form.password_again.data:
            context['message'] = "Пароли не совпадают"
            return render_template('auth/profile.html', **context)
        if db_sess.query(User).filter(User.email == form.email.data).first():
            context['message'] = "Такой email уже занят"
            return render_template('auth/profile.html', **context)
        if db_sess.query(User).filter(
                User.username == form.username.data).first():
            context['message'] = 'Такой username уже занят'
            return render_template('auth/profile.html', **context)

        if user:
            user.username = form.username.data
            user.email = form.email.data
            user.last_name = form.last_name.data
            user.first_name = form.first_name.data
            user.set_password(form.password.data)
            db_sess.commit()
            return redirect('/auth/profile')
    return render_template('auth/profile.html', **context)


@app.route('/quizzes/create')
@login_required
def quiz_create():
    form = QuizCreateForm()
    context = {
        'form': form,
        'title': 'Create quiz',
    }
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        quiz = db_sess.query(Quiz).filter(
            Quiz.title == form.title.data).first()
        if quiz:
            context['message'] = 'Quiz с таким названием уже существует'
            render_template('quizzes/quiz_create.html', **context)
        quiz = Quiz(
            title=form.title.data,
            text=form.text.data,
            owner_id=current_user.id,
        )
        quiz.questions = dumps(form.pages)
        db_sess.commit()
        redirect(f'/quizzes/{quiz.id}/')
    render_template('quizzes/quiz_create.html', **context)


@app.route('/quizzes/<int:pk>/delete', methods=['GET', 'POST'])
@login_required
def quiz_delete(pk):
    context = {
        'title': 'Quiz_delete'
    }
    db_sess = db_session.create_session()
    quiz = db_sess.query(Quiz).filter(Quiz.id == pk).first()
    if not quiz:
        context['message'] = 'Такой Quiz не найден'
        return render_template('quizzes/quizz_delete.html', **context)
    if quiz and quiz.owner_id == current_user.id:
        db_sess.delete(quiz)
        db_sess.commit()
        redirect('/quizzes/success/delete')
    else:
        context['message'] = 'Вы не создатель этого вопроса'
        return render_template('quizzes/quiz_delete.html', **context)
    return render_template('quizzes/quiz_delete.html', **context)


@app.route('/quizzes/success/delete')
def quiz_success_delete():
    context = {
        'title': 'Успешное удаление'
    }
    render_template('quizzes/quiz_success_delete.html')


@app.route('/quizzes/<int:pk>/edit', methods=['GET', 'POST'])
@login_required
def quiz_edit(pk):
    form = QuizEditForm()
    db_sess = db_session.create_session()
    quiz = db_sess.query(Quiz).filter(Quiz.id == pk)
    context = {
        'title': str(quiz.title) + 'edit'
    }
    if form.validate_on_submit():
        if quiz and quiz.owner_id == current_user.id:
            quiz.title = form.title.data
            quiz.text = form.text.data
            quiz.questions = dumps(form.pages)

            db_sess.commit()
        context['message'] = 'У вас нет доступа'
        render_template('quizzes/quiz_edit.html', **context)
    render_template('quizzes/quiz_edit.html', **context)


@app.route('/quizzes/<int:pk>/')
def quiz_info(pk):
    db_sess = db_session.create_session()
    quiz = db_sess.query(Quiz).filter(Quiz.id == pk).first()
    context = {
        'title': str(quiz.title),
    }
    if not quiz:
        abort(404)
    context['quiz'] = quiz
    return render_template('quizzes/quiz_info.html', **context)


@app.route('/quizzes/')
def quizzes_list():
    context = {
        'title': 'List of Quizzes',
    }
    db_sess = db_session.create_session()
    quizzes = db_sess.query(Quiz).all()
    context['quizzes'] = quizzes
    return render_template('quizzes/quizzes_lis.html', **context)


@app.route('/quizzes/<int:pk>/passing/<int:qn>')  # Question num
def quiz_pass(pk, qn):
    db_sess = db_session.create_session()
    quiz = db_sess.query(Quiz).filter(Quiz.id == pk).first()
    questions = loads(quiz.questions)
    print(questions)
    quest = questions[qn]
    context = {
        'title': str(quiz.title),
        'quest': quest
    }
    render_template('quizzes/quiz_pass.html', **context)


def main():
    db_session.global_init("db/balmoot.db")
    app.debug = True
    app.run(port=8080, host='127.0.0.1')

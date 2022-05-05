import os
from io import BytesIO
from json import loads, dumps

from PIL import Image
from flask import Flask, app, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user
from flask_restful import Api

from data import db_session, quiz_resources
from data.forms import LoginForm, RegisterForm, EditForm, QuizCreateForm, \
    QuizEditForm, QuizPassingForm
from data.quiz_db import Quiz
from data.user_db import User

with open('passers.json') as file:
    passing = loads(file.read())

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
        if db_sess.query(User).filter(
                User.username == form.username.data).first():
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
            user.username = form.username.data or user.username
            user.email = form.email.data or user.email
            user.last_name = form.last_name.data or user.last_name
            user.first_name = form.first_name.data or user.first_name
            if form.password.data:
                user.set_password(form.password.data)
            db_sess.commit()
            return redirect('/auth/profile')
    return render_template('auth/profile.html', **context)


@app.route('/quizzes/create', methods=['GET', 'POST'])
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
            return render_template('quizzes/quiz_create.html', **context)
        quiz = Quiz(
            title=form.title.data,
            text=form.text.data,
            owner_id=current_user.id,
        )
        directory = os.path.join(f'{os.getcwd()}/static/img/',
                                 'users_pictures')
        if not os.path.exists(directory):
            os.mkdir(directory)
        f = form.picture.data
        if f:
            im = Image.open(BytesIO(f.read()))
            im.save(os.getcwd().replace('\\', '/') +
                    f"/static/img/users_pictures/quizz_{quiz.title}_picture.png")
            quiz.picture_path = \
                f"/static/img/users_pictures/quizz_{quiz.title}_picture.png"
        questions = [
            [form.question1.data, [form.option_1_1.data, form.option_1_2.data,
                                   form.option_1_3.data,
                                   form.option_1_4.data]],
            [form.question2.data, [form.option_2_1.data, form.option_2_2.data,
                                   form.option_2_3.data,
                                   form.option_2_4.data]],
            [form.question3.data, [form.option_3_1.data, form.option_3_2.data,
                                   form.option_3_3.data,
                                   form.option_3_4.data]],
            [form.question4.data, [form.option_4_1.data, form.option_4_2.data,
                                   form.option_4_3.data,
                                   form.option_4_4.data]],
            [form.question5.data, [form.option_5_1.data, form.option_5_2.data,
                                   form.option_5_3.data,
                                   form.option_5_4.data]]]
        quiz.questions = dumps(questions)
        quiz.answers = form.answers.data
        db_sess.add(quiz)
        db_sess.commit()
        return redirect(f'/quizzes/{quiz.id}/')
    return render_template('quizzes/quiz_create.html', **context)


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
        return render_template('quizzes/quiz_delete.html', **context)
    if quiz and quiz.owner_id == current_user.id:
        db_sess.delete(quiz)
        db_sess.commit()
        return redirect('/quizzes/success/delete')
    else:
        context['message'] = 'Вы не создатель этого вопроса'
        return render_template('quizzes/quiz_delete.html', **context)


@app.route('/quizzes/success/delete')
def quiz_success_delete():
    context = {
        'title': 'Успешное удаление'
    }
    return render_template('quizzes/quiz_success_delete.html')


@app.route('/quizzes/<int:pk>/edit', methods=['GET', 'POST'])
@login_required
def quiz_edit(pk):
    form = QuizEditForm()
    db_sess = db_session.create_session()
    quiz = db_sess.query(Quiz).filter(Quiz.id == pk).first()
    context = {
        'form': form,
        'title': 'quiz_edit',
    }
    if not quiz:
        abort(404)
    context['title'] = str(quiz.title) + ' edit'
    if form.validate_on_submit():
        if quiz.owner_id == current_user.id or quiz.owner_id:
            quiz.title = form.title.data or quiz.title
            quiz.text = form.text.data or quiz.title
            quests = loads(quiz.questions)
            questions = [[form.question1.data or quests[0][0],
                          [form.option_1_1.data or quests[0][1][0],
                           form.option_1_2.data or quests[0][1][1],
                           form.option_1_3.data or quests[0][1][2],
                           form.option_1_4.data or quests[0][1][3]]],
                         [form.question2.data or quests[1][0],
                          [form.option_2_1.data or quests[1][1][0],
                           form.option_2_2.data or quests[1][1][1],
                           form.option_2_3.data or quests[1][1][2],
                           form.option_2_4.data or quests[1][1][3]]],
                         [form.question3.data or quests[2][0],
                          [form.option_3_1.data or quests[2][1][0],
                           form.option_3_2.data or quests[2][1][1],
                           form.option_3_3.data or quests[2][1][2],
                           form.option_3_4.data or quests[2][1][3]]],
                         [form.question4.data or quests[3][0],
                          [form.option_4_1.data or quests[3][1][0],
                           form.option_4_2.data or quests[3][1][1],
                           form.option_4_3.data or quests[3][1][2],
                           form.option_4_4.data or quests[3][1][3]]],
                         [form.question5.data or quests[4][0],
                          [form.option_5_1.data or quests[4][1][0],
                           form.option_5_2.data or quests[4][1][1],
                           form.option_5_3.data or quests[4][1][2],
                           form.option_5_4.data or quests[4][1][3]]]]
            quiz.questions = dumps(questions)
            quiz.answers = form.answers.data or quiz.answers
            f = form.picture.data
            if f:
                im = Image.open(BytesIO(f.read()))
                im.save(
                    os.getcwd().replace('\\', '/') +
                    f"/static/img/users_pictures/quizz_{quiz.title}_picture.png")
                quiz.picture_path = \
                    f"/static/img/users_pictures/quizz_{quiz.title}_picture.png"
            db_sess.commit()
            return redirect(f'/quizzes/{quiz.id}/')
        context['message'] = 'У вас нет доступа'
        return render_template('quizzes/quiz_edit.html', **context)
    return render_template('quizzes/quiz_edit.html', **context)


@app.route('/quizzes/<int:pk>/')
def quiz_info(pk):
    db_sess = db_session.create_session()
    quiz = db_sess.query(Quiz).filter(Quiz.id == pk).first()
    context = {
        'title': 'quiz_info',
    }
    if not quiz:
        abort(404)
    context['title'] = str(quiz.title)
    context['quiz'] = quiz
    context['questions'] = loads(quiz.questions)
    return render_template('quizzes/quiz_info.html', **context)


@app.route('/quizzes/')
def quizzes_list():
    context = {
        'title': 'List of Quizzes',
    }
    db_sess = db_session.create_session()
    quizzes = db_sess.query(Quiz).all()
    context['quizzes'] = quizzes
    return render_template('quizzes/quizzes_list.html', **context)


@app.route('/quizzes/<int:pk>/passing/<int:qn>', methods=['GET', 'POST'])
@login_required
def quiz_pass(pk, qn):
    form = QuizPassingForm()
    context = {
        'form': form,
        'title': 'passing'
    }
    db_sess = db_session.create_session()
    quiz = db_sess.query(Quiz).filter(Quiz.id == pk).first()
    if not quiz or qn > 4 or qn < 0:
        abort(404)
    if form.validate_on_submit():
        if passing.get(str(current_user.id), False):
            passing[str(current_user.id)][str(pk)][qn] = form.response.data
        else:
            passing[str(current_user.id)] = {str(pk): [0, 0, 0, 0, 0]}
        passing[str(current_user.id)][str(pk)][qn] = form.response.data
        if qn != 4:
            return redirect(f'/quizzes/{pk}/passing/{qn + 1}')
        return redirect(f'/quizzes/{pk}/passed')

    questions = loads(quiz.questions)
    quest = questions[qn]
    context['title'] = str(quiz.title)
    context['quest'] = quest
    return render_template('quizzes/quiz_pass.html', **context)


@app.route('/quizzes/<int:pk>/passed')
@login_required
def quiz_passed(pk):
    context = {
        'title': 'Quizz_passed',
    }
    db_sess = db_session.create_session()
    quiz = db_sess.query(Quiz).get(pk)
    if not quiz:
        abort(404)
    with open('passers.json', 'w') as file:
        file.write(dumps(passing))
    context['pass_stat'] = passing[str(current_user.id)][str(pk)]
    context['title'] = quiz.title
    context['quiz'] = quiz
    if not quiz.passers:
        quiz.passers = str(current_user.id)
    if str(current_user.id) not in quiz.passers.split():
        quiz.passers = str(quiz.passers) + ' ' + str(current_user.id)
    db_sess.commit()
    return render_template('quizzes/quiz_passed.html', **context)


def main():
    directory = os.path.join(os.getcwd(), 'db')
    if not os.path.exists(directory):
        os.mkdir(directory)
    db_session.global_init("db/balmoot.db")
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


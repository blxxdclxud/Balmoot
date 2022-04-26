from flask import Flask, app, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.forms import LoginForm
from data.user_db import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuPer-UltrA_seKretNiy_kluCH'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def main_page():
    return render_template('main_pages/main_page.html', title='Main page')


@app.route('auth/register/')
def register():
    return render_template('auth/register.html', title='Register')


@LoginManager.user_loader
def load_user(pk):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(pk)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.username_or_email == form.username_or_email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('auth/login.html', title='Login', form=form)


@app.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    app.run()

from flask import Flask
from flask import app
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def main_page():
    return render_template('main_pages/main_page.html', title='Main page')


@app.route('/register/')
def register():
    return render_template('auth/register.html', title='Register')


@app.route('/login/')
def login():
    return render_template('auth/login.html', title='Login')


def main():
    app.run()

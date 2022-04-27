from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, \
    BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Enter your email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password',
                                   validators=[DataRequired()])
    last_name = StringField('Surname', validators=[DataRequired()])
    first_name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    username_or_email = StringField('Username or email',
                                   validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Log in')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Enter your email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password',
                                   validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    first_name = StringField('First_name', validators=[DataRequired()])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    username_or_email = StringField('Username or email',
                                    validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Log in')


class EditForm(FlaskForm):
    username = StringField('Username')
    email = EmailField('Enter your email')
    password = PasswordField('Password')
    password_again = PasswordField('Repeat password')
    last_name = StringField('Last_name')
    first_name = StringField('First_name')
    submit = SubmitField('Edit')


class QuizCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = StringField('Description')

    pages = []
    for i in range(100):
        ask = {
            'question': StringField(f''),
            'options': [StringField(f'Option-0-{i}'),
                        StringField(f'Option-1-{i}'),
                        StringField(f'Option-2-{i}'),
                        StringField(f'Option-3-{i}')]
        }
        pages.append(ask)


class QuizEditForm(FlaskForm):
    title = StringField('Title')
    text = StringField('Description')
    pages = []
    for i in range(100):
        ask = {
            'question': StringField(f''),
            'options': [StringField(f'Option-0-{i}'),
                        StringField(f'Option-1-{i}'),
                        StringField(f'Option-2-{i}'),
                        StringField(f'Option-3-{i}')]
        }
        pages.append(ask)

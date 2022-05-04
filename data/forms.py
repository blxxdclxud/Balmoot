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

    question1 = StringField('Question1', validators=[DataRequired()])
    option_1_1 = StringField('Option 1', validators=[DataRequired()])
    option_1_2 = StringField('Option 2', validators=[DataRequired()])
    option_1_3 = StringField('Option 3', validators=[DataRequired()])
    option_1_4 = StringField('Option 4', validators=[DataRequired()])

    question2 = StringField('Question2', validators=[DataRequired()])
    option_2_1 = StringField('Option 1', validators=[DataRequired()])
    option_2_2 = StringField('Option 2', validators=[DataRequired()])
    option_2_3 = StringField('Option 3', validators=[DataRequired()])
    option_2_4 = StringField('Option 4', validators=[DataRequired()])

    question3 = StringField('Question3', validators=[DataRequired()])
    option_3_1 = StringField('Option 1', validators=[DataRequired()])
    option_3_2 = StringField('Option 2', validators=[DataRequired()])
    option_3_3 = StringField('Option 3', validators=[DataRequired()])
    option_3_4 = StringField('Option 4', validators=[DataRequired()])

    question4 = StringField('Question4', validators=[DataRequired()])
    option_4_1 = StringField('Option 1', validators=[DataRequired()])
    option_4_2 = StringField('Option 2', validators=[DataRequired()])
    option_4_3 = StringField('Option 3', validators=[DataRequired()])
    option_4_4 = StringField('Option 4', validators=[DataRequired()])

    question5 = StringField('Question5', validators=[DataRequired()])
    option_5_1 = StringField('Option 1', validators=[DataRequired()])
    option_5_2 = StringField('Option 2', validators=[DataRequired()])
    option_5_3 = StringField('Option 3', validators=[DataRequired()])
    option_5_4 = StringField('Option 4', validators=[DataRequired()])

    answers = StringField('Ответы (писать через пробел)',
                          validators=[DataRequired()])

    submit = SubmitField('Create')


class QuizEditForm(FlaskForm):
    title = StringField('Title')
    text = StringField('Description')

    question1 = StringField('Question1')
    option_1_1 = StringField('Option 1')
    option_1_2 = StringField('Option 2')
    option_1_3 = StringField('Option 3')
    option_1_4 = StringField('Option 4')

    question2 = StringField('Question2')
    option_2_1 = StringField('Option 1')
    option_2_2 = StringField('Option 2')
    option_2_3 = StringField('Option 3')
    option_2_4 = StringField('Option 4')

    question3 = StringField('Question3')
    option_3_1 = StringField('Option 1')
    option_3_2 = StringField('Option 2')
    option_3_3 = StringField('Option 3')
    option_3_4 = StringField('Option 4')

    question4 = StringField('Question4')
    option_4_1 = StringField('Option 1')
    option_4_2 = StringField('Option 2')
    option_4_3 = StringField('Option 3')
    option_4_4 = StringField('Option 4')

    question5 = StringField('Question5')
    option_5_1 = StringField('Option 1')
    option_5_2 = StringField('Option 2')
    option_5_3 = StringField('Option 3')
    option_5_4 = StringField('Option 4')

    answers = StringField('Ответы (писать через пробел)')

    submit = SubmitField('Edit')

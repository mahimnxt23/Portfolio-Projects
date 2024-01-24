from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    submit = SubmitField('Sign Up!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login!')


class ToDoListForm(FlaskForm):
    date = DateField('Task Date', validators=[InputRequired()])
    work_todo = StringField('Work which needs to be done...', validators=[InputRequired()])
    submit = SubmitField('Set the Task!')


# as of now, these will do...

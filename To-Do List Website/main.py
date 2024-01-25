from datetime import datetime, timezone
from forms import RegisterForm, LoginForm, ToDoListForm
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from sqlalchemy import String, Integer, Boolean, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Relationship
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


current_year = datetime.now().year

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i_am_the_super_secure_key!'
Bootstrap(app=app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to-do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(model_class=Base)
db.init_app(app=app)

login_manager = LoginManager()
login_manager.init_app(app=app)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    # insert analog way here later...

    def __repr__(self):
        return f'<User {self.username}>'


class TodoList(db.Model):
    __tablename__ = 'todolist'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    todo: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # insert analog way here later...

    def __repr__(self):
        return f'Todo_list{self.todo}'


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/')
def home_page():
    return render_template('index.html', year=current_year)


@app.route('/sign-up', methods=['GET', 'POST'])
def register_page():
    register_form = RegisterForm()

    entered_username = register_form.username.data
    entered_password = register_form.password.data
    entered_email = register_form.email.data

    if register_form.validate_on_submit():
        if User.query.filter_by(email=entered_email).first():
            flash(message='You\'ve already signed up with this email, consider logging in...')
            return redirect(url_for('login_page'))

        encrypted_password = generate_password_hash(entered_password, method='pbkdf2:sha256', salt_length=8)

        new_user = User(username=entered_username, password=encrypted_password, email=entered_email)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home_page'))
    return render_template('register.html', form=register_form,
                           current_user=current_user, year=current_year)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        entered_email = login_form.email.data
        entered_password = login_form.password.data
        this_user = User.query.filter_by(email=entered_email).first()

        if not this_user:
            flash(message=f'This email({entered_email}) does not exist. Please check and try again!')
            return redirect(url_for('login_page'))

        elif not check_password_hash(this_user.password, entered_password):
            flash(message='Oh no! You might have mistaken the password. Because it does not match.')
            return redirect(url_for('login_page'))

        else:
            login_user(this_user)
            return redirect(url_for('home_page'))

    return render_template('login.html', form=login_form, year=current_year)


@app.route('/setup-todo', methods=['GET', 'POST'])
def create_task():
    todo_form = ToDoListForm()

    if todo_form.validate_on_submit():
        new_todo = TodoList(date=todo_form.date.data, todo=todo_form.work_todo.data)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('to-do.html', form=todo_form, year=current_year)


if __name__ == '__main__':
    app.run(debug=True)

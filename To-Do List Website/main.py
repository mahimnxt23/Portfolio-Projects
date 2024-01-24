from datetime import datetime
from forms import RegisterForm, LoginForm, ToDoListForm
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from sqlalchemy import String, Integer, Boolean, Float, Text, ForeignKey
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


@app.route('/')
def home_page():
    return render_template('index.html', year=current_year)


if __name__ == '__main__':
    app.run(debug=True)

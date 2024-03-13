from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer


app = Flask(__name__)
app.config['SECRET_KEY'] = 'i_am_the_super_secure_key!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app=app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app=app)


# everything needs to set up here. check keep notes apps...

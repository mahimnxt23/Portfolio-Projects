from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from stripe import *


# initial settings...
app = Flask(__name__)
app.config["SECRET_KEY"] = "a_super_secure_key!"
Bootstrap(app=app)


class Base(DeclarativeBase):
    pass


# CONNECTING TO DB...
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(model_class=Base)
db.init_app(app=app)


# login functionalities...
login_manager = LoginManager()
login_manager.init_app(app=app)

api_key = 'sk_test_51OtY3LCUs5SzWLs8KvITVYikf2LLj9jlMnbst5cF6inFg7mhhO7rmymxzK1rTgQcuxOmWj114fKia9cezQm2PXox00cAG3d3kz'
cart_items = []


# everything needs to set up here. check keep notes apps...
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    cart_items = relationship("Cart", back_populates="user", lazy=True)


class EshopItem(db.Model):
    __tablename__ = "eshop_item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    stock: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)


class Cart(db.Model):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    items: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


@app.route('/')
def home():
    shop_items = EshopItem.query.all()
    return render_template("index.html", eshop_items=shop_items,
                           logged_in=current_user.is_authenticated)

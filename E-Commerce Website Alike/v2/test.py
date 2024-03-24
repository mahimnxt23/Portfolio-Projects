from flask import Flask, render_template
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email


# app initialization...
app = Flask(__name__)
app.config["SECRET_KEY"] = "a-super-secure-key"
Bootstrap(app)


# db setup...
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# db classes preparation...
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    
    cart_items = db.relationship("Cart", backref="user", lazy=True)
    
    
class EshopItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    name = db.Column(db.String(100))
    image = db.Column(db.String)
    description = db.Column(db.Text(10000))
    stock = db.Column(db.Integer)
    price = db.Column(db.Float)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    
class RegisterUserForm(FlaskForm):
    name = StringField('USERNAME', validators=[InputRequired()])
    email = StringField('EMAIL', validators=[InputRequired(), Email()])
    password = PasswordField('PASSWORD', validators=[InputRequired()])
    submit = SubmitField('Register Me!')


class LoginUserForm(FlaskForm):
    email = StringField("EMAIL", validators=[InputRequired(), Email()])
    password = PasswordField('PASSWORD', validators=[InputRequired()])
    submit = SubmitField('Let Me In!')


@app.route("/")
def homepage():
    eshop_items = EshopItem.query.all()
    return render_template("index.html", eshop_items=eshop_items)


@app.route("/detail/<int:item_id>/")
def product_detail(item_id):
    item_to_show = EshopItem.query.filter_by(id=item_id).first()
    return render_template("product-detail.html", item=item_to_show)


@app.route("/register")
def register_page():
    register_form = RegisterUserForm()
    return render_template("register.html", form=register_form)


@app.route("/login")
def login_page():
    login_form = LoginUserForm()
    return render_template("login.html", form=login_form)


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/shop-cart")
def shop_cart():
    return render_template("shop-cart.html")


if __name__ == "__main__":
    app.run(port=5010, debug=True)

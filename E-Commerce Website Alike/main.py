from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import stripe


app = Flask(__name__)
app.config["SECRET_KEY"] = "a-super-secure-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


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


login_manager = LoginManager()
login_manager.init_app(app)

TEST_KEY = "sk_test_51OtY3LCUs5SzWLs8KvITVYikf2LLj9jlMnbst5cF6inFg7mhhO7rmymxzK1rTgQcuxOmWj114fKia9cezQm2PXox00cAG3d3kz"
stripe.api_key = TEST_KEY

items_in_cart = []


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CREATE TABLE
# db.create_all()


@app.route("/")
def home():
    eshop_items = EshopItem.query.all()
    return render_template(
        "index.html", logged_in=current_user.is_authenticated, eshop_items=eshop_items
    )


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        items_in_cart=items_in_cart,
        mode="payment",
        success_url="http://127.0.0.1:5000/success/",
        cancel_url="https://templates/cancel.html",
    )

    return redirect(session.url, code=303)


@app.route("/success/")
def success():
    return render_template("success.html", user=current_user, items=items_in_cart)


def calculate_final_price():
    global items_in_cart
    items_in_cart = []
    price = 0.0
    cart_user_items = Cart.query.filter_by(user_id=current_user.id).all()
    for item in cart_user_items:
        price += float(EshopItem.query.filter_by(id=item.items).first().price) * float(
            item.quantity
        )
        items_in_cart.append(
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": EshopItem.query.filter_by(id=item.items).first().name,
                    },
                    "unit_amount": int(
                        str(int(EshopItem.query.filter_by(id=item.items).first().price))
                        + "00"
                    ),
                },
                "quantity": item.quantity,
            },
        )
        return price


@app.route("/detail/<item_id>")
def detail(item_id):
    item = EshopItem.query.filter_by(id=item_id).first()
    return render_template(
        "detail.html", logged_in=current_user.is_authenticated, item=item
    )


@app.route("/cart/")
def cart():
    final_price = calculate_final_price()
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    eshop_items = EshopItem.query.all()
    return render_template(
        "cart.html",
        logged_in=current_user.is_authenticated,
        cart_items=cart_items,
        eshop_items=eshop_items,
        final_price=final_price,
    )


@app.route("/add_to_cart/<item_id>")
def add_to_cart(item_id):
    if is_item_in_cart(item_id):
        item_to_update = Cart.query.filter_by(items=item_id).first()
        item_to_update.quantity += 1
        db.session.commit()
    else:
        new_card_record = Cart(items=item_id, quantity=1, user_id=current_user.id)
        db.session.add(new_card_record)
        db.session.commit()
    return redirect(url_for("home"))


def is_item_in_cart(item_id):
    cart_user_items = Cart.query.filter_by(user_id=current_user.id).all()
    for item in cart_user_items:
        if int(item.items) == int(item_id):
            return item.id
        else:
            return False


@app.route("/delete_from_cart/<item_id>")
def delete_from_cart(item_id):
    item_to_delete = Cart.query.get(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for("cart"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if User.query.filter_by(email=request.form.get("email")).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))

        hash_and_salted_password = generate_password_hash(
            request.form.get("password"), method="pbkdf2:sha256", salt_length=8
        )
        # noinspection PyArgumentList
        new_user = User(
            email=request.form.get("email"),
            name=request.form.get("name"),
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("home"))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(port=5001, debug=True)

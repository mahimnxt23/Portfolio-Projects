from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash


# app initialization...
app = Flask(__name__)
app.config["SECRET_KEY"] = "a-super-secure-key"
csrf = CSRFProtect(app)
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
    items_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    
# with app.app_context():
#     db.create_all()
    
    
class RegisterUserForm(FlaskForm):
    name = StringField('USERNAME', validators=[InputRequired()])
    email = StringField('EMAIL', validators=[InputRequired(), Email()])
    password = PasswordField('PASSWORD', validators=[InputRequired()])
    submit = SubmitField('Register Me!')


class LoginUserForm(FlaskForm):
    email = StringField("EMAIL", validators=[InputRequired(), Email()])
    password = PasswordField('PASSWORD', validators=[InputRequired()])
    submit = SubmitField('Let Me In!')


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    register_form = RegisterUserForm()
    password = register_form.password.data
    
    if register_form.validate_on_submit():
        
        if User.query.filter_by(email=register_form.email.data).first():  # User already exists...
            flash(message='You\'ve already signed up with this email, consider logging in...')
            return redirect(url_for('login_page'))
        
        hashed_and_salted_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        # noinspection PyArgumentList
        new_user = User(
            email=register_form.email.data,
            name=register_form.name.data.title(),
            password=hashed_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)  # logs in immediately...
        return redirect(url_for('homepage'))
            
    return render_template("register.html", form=register_form, this_user=current_user)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    login_form = LoginUserForm()
    
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash(message=f'This email({email}) does not exist. Please check and try again!')
            
        elif not check_password_hash(user.password, password):
            flash(message='Oh no! You have mistaken the password. Did you forget your precious password?')
            
        else:
            login_user(user)
            return redirect(url_for('homepage'))
        
    return render_template("login.html", form=login_form, this_user=current_user)


@app.route("/logout")
@login_required
def outcast_user():
    logout_user()
    return redirect(url_for('homepage'))


@app.route("/", methods=['GET'])
def homepage():
    eshop_items = EshopItem.query.all()
    return render_template("index.html", eshop_items=eshop_items, this_user=current_user)


@app.route("/detail/<int:item_id>", methods=['GET'])
def product_detail(item_id):
    item_to_show = EshopItem.query.filter_by(id=item_id).first()
    return render_template("product-detail.html", item=item_to_show, this_user=current_user)


@app.route("/update_cart/<int:item_id>", methods=['GET', 'POST'])
def update_cart(item_id):
    quantity = int(request.form.get('quantity', 1))  # capturing incoming value through AJAX & converting to integer...
    buying_item = EshopItem.query.filter_by(id=item_id).first()
    
    if not buying_item or buying_item.stock < quantity:
        return jsonify({'status': 'fail', 'error': 'Not enough stock available!'})
        # return jsonify({'status': 'fail', 'error': 'I have have failed you MASTER [ 1 ]'})
    
    if item_already_in_cart(item_id):
        item_to_update = Cart.query.filter_by(items_id=item_id, user_id=current_user.id).first()
        
        if item_to_update:
            if quantity > buying_item.stock:
                return jsonify({'status': 'fail', 'error': 'Not enough stock available'})
                # return jsonify({'status': 'fail', 'error': 'I have have failed you MASTER [ 2 ]'})
            
            item_to_update.quantity += quantity
            buying_item.stock -= quantity
            db.session.commit()
            return jsonify({'status': 'success', 'item_id': item_id, 'quantity_added': quantity})
        
    else:
        # noinspection PyArgumentList
        new_cart_record = Cart(items_id=item_id, quantity=quantity, user_id=current_user.id)
        db.session.add(new_cart_record)
        buying_item.stock -= quantity
        db.session.commit()
        
    return jsonify({'status': 'success', 'item_id': item_id, 'quantity_added': quantity})


def item_already_in_cart(item_id):
    user_cart_items = Cart.query.filter_by(items_id=item_id, user_id=current_user.id).first()
    return user_cart_items is not None


@app.route("/checkout", methods=['GET'])
def checkout():
    return render_template("checkout.html", this_user=current_user)


def calculate_total_checkout_price(from_shop, from_cart):
    subtotal_price, total_price, delivery_cost = (float(0), float(0), float(99))
    
    for shop_item in from_shop:
        for cart_item in from_cart:
            if shop_item.id == cart_item.items_id:
                subtotal_price += float(shop_item.price * cart_item.quantity)
                
    if not subtotal_price >= float(500):
        total_price = float(subtotal_price + delivery_cost)
    else:
        total_price = subtotal_price
    
    return subtotal_price, total_price


@app.route("/shop-cart", methods=['GET'])
def shop_cart():
    
    if current_user.is_authenticated:
        items_in_cart = Cart.query.filter_by(user_id=current_user.id).all()
        items_in_shop = EshopItem.query.all()
        checkout_prices = calculate_total_checkout_price(items_in_shop, items_in_cart)
        
        return render_template("shop-cart.html", this_user=current_user, eshop_items=items_in_shop,
                               cart_items=items_in_cart, final_prices=checkout_prices)
    else:
        return redirect(url_for('login_page'))


if __name__ == "__main__":
    app.run(port=5010, debug=True)

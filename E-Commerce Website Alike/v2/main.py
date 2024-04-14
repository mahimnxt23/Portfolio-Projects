from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from dotenv import load_dotenv
from sqlalchemy import func
from pprint import pprint
from os import getenv
import stripe
import json


# app initialization...
app = Flask(__name__)
app.config["SECRET_KEY"] = getenv('SEQURITY_KEY')
csrf = CSRFProtect(app)
Bootstrap(app)


# db setup...
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# db.init_app(app)

load_dotenv()
stripe.api_key = getenv('STRIPE_API_KEY')


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


class RegisterUserForm(FlaskForm):
    name = StringField('USERNAME', validators=[InputRequired()])
    email = StringField('EMAIL', validators=[InputRequired(), Email()])
    password = PasswordField('PASSWORD', validators=[InputRequired()])
    submit = SubmitField('Register Me!')


class LoginUserForm(FlaskForm):
    email = StringField("EMAIL", validators=[InputRequired(), Email()])
    password = PasswordField('PASSWORD', validators=[InputRequired()])
    submit = SubmitField('Let Me In!')


class UserDetails:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items_in_cart = self.get_items_from_cart_by_id()
        self.items_in_shop = self.get_all_items_from_shop()
        self.purchasing_item_details = self.serve_cart_items_to_stripe()
        self.user_unique_items_count = self.get_unique_product_cart_items_count()
        self.user_cart_items_count = self.get_total_cart_items_count()
    
    def get_items_from_cart_by_id(self):
        return Cart.query.filter_by(user_id=self.user_id).all()
    
    # noinspection PyMethodMayBeStatic
    def get_all_items_from_shop(self):
        return EshopItem.query.all()
    
    def calculate_purchasing_cost(self):
        
        if not self.items_in_cart:
            return 0, 0, 0
        
        else:
            item_prices = {item.id: item.price for item in self.items_in_shop}
            item_quantities = {item.items_id: item.quantity for item in self.items_in_cart}
            
            subtotal_price = sum(item_prices[item_id] * quantity for item_id, quantity in item_quantities.items())
            delivery_cost = 199 if subtotal_price < 499 else 0
            total_price = subtotal_price + delivery_cost
            
            return subtotal_price, delivery_cost, total_price
        
    def serve_cart_items_to_stripe(self):
        shop_items = {item.id: item for item in self.items_in_shop}
        cart_items = self.items_in_cart
        
        return [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': shop_items[cart_item.items_id].name,
                    },
                    'unit_amount': int(round(shop_items[cart_item.items_id].price * 100)),
                },
                'quantity': cart_item.quantity,
            }
            for cart_item in cart_items if cart_item.items_id in shop_items
        ]
    
    def get_unique_product_cart_items_count(self):
        return len(self.items_in_cart)
    
    def get_total_cart_items_count(self):
        return db.session.query(func.sum(Cart.quantity)).filter(Cart.user_id == self.user_id).scalar()
    

# with app.app_context():
#     db.create_all()


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


@app.route("/add_to_cart/<int:item_id>", methods=['GET', 'POST'])
def add_to_cart(item_id):
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


@app.route("/shop-cart", methods=['GET', 'POST'])
def shop_cart():
    try:
        if current_user.is_authenticated:
            user_info = UserDetails(current_user.id)
            cart_items = user_info.items_in_cart
            shop_items = user_info.items_in_shop
            checkout_prices = user_info.calculate_purchasing_cost()
            
            return render_template("shop-cart.html", this_user=current_user, eshop_items=shop_items,
                                   cart_items=cart_items, final_prices=checkout_prices)
        else:
            return redirect(url_for('login_page'))
        
    except Exception as e:
        return str(e), 500
    
    
@app.route('/update_cart', methods=['GET', 'POST'])
def update_cart():
    updates = request.form.get('updates')
    updates = json.loads(updates)

    for update in updates:
        item_id = update['item_id']
        increase = int(update['increase'])
        decrease = int(update['decrease'])
        delete_from_cart = update['deleted']

        selected_product_in_shop = EshopItem.query.filter_by(id=item_id).first()
        selected_product_in_cart = Cart.query.filter_by(items_id=item_id, user_id=current_user.id).first()
        
        current_stock = selected_product_in_shop.stock
        current_quantity = selected_product_in_cart.quantity
        
        # noinspection PyUnusedLocal
        def set_values_for(mode):
            
            if mode == 'update':
                selected_product_in_shop.stock = current_stock - increase + decrease
                selected_product_in_cart.quantity = current_quantity + increase - decrease
                
            elif mode == 'reduce_quantity':
                selected_product_in_shop.stock = current_stock + current_quantity
                selected_product_in_cart.quantity = 0
                db.session.delete(selected_product_in_cart)
                
            elif mode == 'wipe_from_cart':
                selected_product_in_shop.stock += current_quantity
                selected_product_in_cart.quantity = 0
                db.session.delete(selected_product_in_cart)
        
        decrease_amount = (current_quantity - decrease + increase)
        
        if 1 <= increase <= current_stock:
            set_values_for(mode='update')
            
        elif decrease >= 1 and decrease_amount > 0:
            set_values_for(mode='update')
            
        elif decrease_amount <= 0:
            set_values_for(mode='reduce_quantity')
            
        elif delete_from_cart:
            set_values_for(mode='wipe_from_cart')
            
        else:
            print('Update or remove was never executed!')
    
        db.session.commit()
    
    return jsonify({'status': 'success', 'stats': 'Updated Everything!'})


@app.route("/checkout", methods=['GET', 'POST'])
def checkout_page():
    if current_user.is_authenticated:
        
        user_info = UserDetails(current_user.id)
        cart_items = user_info.items_in_cart
        shop_items = user_info.items_in_shop
        checkout_prices = user_info.calculate_purchasing_cost()
        pprint(user_info.serve_cart_items_to_stripe())
        
        return render_template("checkout.html", this_user=current_user, eshop_items=shop_items,
                               cart_items=cart_items, final_prices=checkout_prices)
    else:
        return redirect(url_for('login_page'))
    
    
@app.route('/create-checkout-stripe_session', methods=['GET', 'POST'])
def checkout_session():
    try:
        user_info = UserDetails(current_user.id)
        items_to_pass = user_info.purchasing_item_details

        stripe_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items_to_pass,
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
        )
        pprint(stripe_session.url)
        # return redirect(stripe_session.url, code=303)
        return jsonify({'status': 'success', 'checkoutUrl': stripe_session.url})
    
    except Exception as e:
        pprint(str(e))
        # return str(e)
        return jsonify({'status': 'error', 'error': str(e)})


@app.route('/success')
@login_required
def success():
    return render_template("success.html", this_user=current_user)


@app.route('/cancel')
@login_required
def cancel():
    return render_template("cancel.html", this_user=current_user)


if __name__ == "__main__":
    app.run(port=5010, debug=True)

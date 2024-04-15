# def calculate_total_checkout_price(from_shop, from_cart):
#     if not from_cart:
#         return 0, 0, 0
#
#     else:
#         item_prices = {item.id: item.price for item in from_shop}
#         item_quantities = {item.items_id: item.quantity for item in from_cart}
#
#         subtotal_price = sum(item_prices[item_id] * quantity for item_id, quantity in item_quantities.items())
#         delivery_cost = 199 if subtotal_price < 599 else 0
#         total_price = subtotal_price + delivery_cost
#
#         return subtotal_price, delivery_cost, total_price
#
#
# @app.route("/shop-cart", methods=['GET', 'POST'])
# def shop_cart():
#     try:
#         if current_user.is_authenticated:
#             items_in_cart = Cart.query.filter_by(user_id=current_user.id).all()
#             items_in_shop = EshopItem.query.all()
#             checkout_prices = calculate_total_checkout_price(items_in_shop, items_in_cart)
#             return render_template("shop-cart.html", this_user=current_user, eshop_items=items_in_shop,
#                                    cart_items=items_in_cart, final_prices=checkout_prices)
#         else:
#             return redirect(url_for('login_page'))
#
#     except Exception as e:
#         return str(e), 500

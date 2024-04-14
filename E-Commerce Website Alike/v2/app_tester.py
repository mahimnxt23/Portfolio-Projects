from main import UserDetails, app, Cart, db
from sqlalchemy import func
from pprint import pprint


user_id = 1


with app.app_context():
    user_info = UserDetails()
    
    def result_1():
        return user_info.get_unique_product_cart_items_count()
    
    pprint(result_1())
    
    def result_2():
        user_cart_items_count = db.session.query(func.sum(Cart.quantity)).filter(Cart.user_id == user_id).scalar()
        return user_cart_items_count

    pprint(result_2())

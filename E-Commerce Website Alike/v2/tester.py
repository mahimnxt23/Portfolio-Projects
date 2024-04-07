from flask_sqlalchemy import SQLAlchemy
from main import app, db, Cart, EshopItem


def serve_cart_items_to_stripe():
    with app.app_context():
        user_id = 1
        items_in_cart = Cart.query.filter_by(id=user_id).all()
        # print(items_in_cart)
        items_in_shop = EshopItem.query.all()
        # print(items_in_shop)
        
        purchasing_items = []
        # Convert items_in_shop to a dictionary for easy lookup
        shop_items_dict = {item.id: item for item in items_in_shop}
        # print(shop_items_dict)
        
        for cart_item in items_in_cart:
            shop_item = shop_items_dict.get(cart_item.items_id)
            if shop_item:
                purchasing_items.append(
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': shop_item.name,
                            },
                            'unit_amount': shop_item.price,
                        },
                        'quantity': cart_item.quantity,
                    }
                )
            else:
                # Handle the case where the item is not found in the shop
                print(f"Item with ID {cart_item.items_id} not found in the shop.")
        
        return purchasing_items


if __name__ == '__main__':
    print(serve_cart_items_to_stripe())

# from main import app, UserDetails
# from pprint import pprint
#
#
# def serve_cart_items_to_stripe():
#
#     with app.app_context():
#         purchasing_items = []
#
#         user_info = UserDetails(user_id=1)
#         cart_items = user_info.items_in_cart
#         shop_items = user_info.items_in_shop
#
#         for shop_item in shop_items:
#             for cart_item in cart_items:
#                 if cart_item.items_id == shop_item.id:
#
#                     purchasing_items.append(
#                         {
#                             'price_data': {
#                                 'currency': 'usd',
#                                 'product_data': {
#                                     'name': shop_item.name,
#                                 },
#                                 'unit_amount': shop_item.price,
#                             },
#                             'quantity': cart_item.quantity,
#                         }
#                     )
#
#         return purchasing_items
#
#
# if __name__ == '__main__':
#     pprint(serve_cart_items_to_stripe())


from main import app, UserDetails
from pprint import pprint


def serve_cart_items_to_stripe():
    with app.app_context():
        user_info = UserDetails(user_id=1)
        cart_items = user_info.items_in_cart
        shop_items = {item.id: item for item in user_info.items_in_shop}
        
        return [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': shop_items[cart_item.items_id].name,
                    },
                    'unit_amount': shop_items[cart_item.items_id].price,
                },
                'quantity': cart_item.quantity,
            }
            for cart_item in cart_items if cart_item.items_id in shop_items
        ]


if __name__ == '__main__':
    pprint(serve_cart_items_to_stripe())

import stripe
from flask import redirect, url_for  # , Flask
from main import UserDetails, app

# app = Flask(__name__)

with app.app_context():
    user_info = UserDetails(user_id=1)
    
    # Set your secret key: remember to change this to your live secret key in production
    stripe.api_key = 'your-secret-key'
    
    
    @app.route('/create-checkout-session', methods=['POST'])
    def create_checkout_session():
        
        try:
            line_items = user_info.purchasing_item_details
    
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=url_for('success', _external=True),
                cancel_url=url_for('cancel', _external=True),
            )
            return redirect(session.url, code=303)
        
        except Exception as e:
            # Handle exceptions
            return str(e)
    
    
    @app.route('/success')
    def success():
        # Handle post-payment success
        return 'Payment succeeded!'
    
    
    @app.route('/cancel')
    def cancel():
        # Handle payment cancellation
        return 'Payment was cancelled.'


if __name__ == '__main__':
    app.run(port=5001, debug=True)

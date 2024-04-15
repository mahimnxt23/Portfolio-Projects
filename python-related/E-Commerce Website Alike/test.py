import stripe
from flask import redirect, request, render_template
from flask_login import current_user

from main import app


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'T-shirt',
                    },
                    'unit_amount': 2000,
                },
                'quantity': 1,
            }],
            mode="payment",
            success_url="http://127.0.0.1:5000/success/",
            cancel_url="https://templates/cancel.html",
        )
        return redirect(session.url, code=303)
    except stripe.error.StripeError as e:
        # Handle error here
        return str(e), 400


@app.route("/success/")
def success():
    # Retrieve the session to display the purchased items
    session_id = request.args.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    items = session.line_items
    return render_template("success.html", user=current_user, items=items)

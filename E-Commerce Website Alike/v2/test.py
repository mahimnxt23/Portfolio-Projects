from flask import Flask, render_template


app = Flask(__name__)
app.config["SECRET_KEY"] = "a-super-secure-key"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/product-details")
def product_details():
    return render_template("product-details.html")


@app.route("/shop")
def shop():
    return render_template("shop.html")


@app.route("/shop-cart")
def shop_cart():
    return render_template("shop-cart.html")


if __name__ == "__main__":
    app.run(debug=True)

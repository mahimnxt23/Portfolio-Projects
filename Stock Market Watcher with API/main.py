from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import requests

MY_API_KEY = "84ff9226e6ae854bc448f2de0157bde5"

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def home():
    responses = requests.get(
        url="http://api.marketstack.com/v1/tickers?",
        params={"access_key": MY_API_KEY},
    )
    coins = responses.json()["data"]
    # print(coins)
    return render_template("main.html", coins=coins)


@app.route("/search")
def search():
    coin = request.args.get("coin")
    if coin:
        responses = requests.get(
            url=f"http://api.marketstack.com/v1/tickers?symbol={coin}",
            params={"access_key": "84ff9226e6ae854bc448f2de0157bde5"},
        )
        responses = responses.json()["data"]
        # print(responses)
        return render_template("main.html", coins=responses)
    else:
        responses = requests.get(
            url="http://api.marketstack.com/v1/tickers?",
            params={"access_key": "84ff9226e6ae854bc448f2de0157bde5"},
        )
    return render_template("main.html", coins=responses)


# @app.route("/end_of_day")
# def end_of_day():
#     coin = request.args.get("coin")
#     eod = requests.get(url=f"http://api.marketstack.com/v1/eod?symbol={coin}",
#     params={"access_key": "84ff9226e6ae854bc448f2de0157bde5"})
#     eod = eod.json()
#     print(eod)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from pprint import pprint
from requests import get


HOME_URL = "http://api.marketstack.com/v1/tickers?"
MY_API_KEY = "84ff9226e6ae854bc448f2de0157bde5"


app = Flask(__name__)
Bootstrap(app)


def serve_api_data(from_url):
    response = get(url=from_url, params={"access_key": MY_API_KEY})
    return response


@app.route("/")
def home():
    coins = serve_api_data(from_url=HOME_URL).json()["data"]
    pprint(coins)
    return render_template("index.html", coins=coins)


@app.route("/search")
def search():
    coin = request.args.get("coin")
    search_url = f"http://api.marketstack.com/v1/tickers?symbol={coin}"

    if coin:
        responses = serve_api_data(from_url=search_url).json()["data"]
        pprint(responses)
        return render_template("coin.html", coins=responses)
    
    else:
        responses = serve_api_data(from_url=HOME_URL).json()["data"]
        return render_template("index.html", coins=responses)


@app.route("/eod")
def end_of_day():
    coin = request.args.get("coin")
    eod_url = f"http://api.marketstack.com/v1/eod?symbol={coin}"
    
    eod = serve_api_data(from_url=eod_url).json()["data"]
    pprint(eod)
    return render_template("eod.html", eod=eod)


if __name__ == "__main__":
    app.run(debug=True)

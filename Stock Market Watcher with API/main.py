from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
# from pprint import pprint
from requests import get


HOME_URL = "http://api.marketstack.com/v1/tickers?"
MY_API_KEY = "84ff9226e6ae854bc448f2de0157bde5"


app = Flask(__name__)
Bootstrap(app)


def get_data_from_api(from_url):
    response = get(url=from_url, params={"access_key": MY_API_KEY})
    return response.json()["data"]


@app.route("/")
def home():
    company_symbols = get_data_from_api(from_url=HOME_URL)
    # pprint(company_symbols)
    return render_template("index.html", company_symbols=company_symbols)


@app.route("/search")
def search():
    company_symbol = request.args.get("company_symbol")
    eod_url = f"http://api.marketstack.com/v1/eod?symbols={company_symbol}"

    if company_symbol:
        responses = get_data_from_api(from_url=eod_url)
        # pprint(responses)
        return render_template("eod.html", company_symbols=responses)

    else:
        responses = get_data_from_api(from_url=HOME_URL)
        return render_template("index.html", company_symbols=responses)


@app.route("/eod")
def end_of_day():
    company_symbol = request.args.get("company_symbol")
    eod_url = f"http://api.marketstack.com/v1/eod?symbols={company_symbol}"

    eod = get_data_from_api(from_url=eod_url)
    # pprint(eod)
    return render_template("eod.html", eod=eod)


if __name__ == "__main__":
    app.run(debug=True)

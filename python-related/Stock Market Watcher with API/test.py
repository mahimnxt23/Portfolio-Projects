from requests import get
from pprint import pprint


HOME_URL = "http://api.marketstack.com/v1/tickers?"
SEARCH_URL = "http://api.marketstack.com/v1/eod?symbols=aapl"
MY_API_KEY = "84ff9226e6ae854bc448f2de0157bde5"


def get_data_from_api(from_url):
    response = get(url=from_url, params={"access_key": MY_API_KEY})
    return response.json()["data"][1]


pprint(get_data_from_api(HOME_URL))
# pprint(get_data_from_api(SEARCH_URL))

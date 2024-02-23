import requests
from bs4 import BeautifulSoup
from pprint import pprint

NUMBER_OF_PAGES = 3
current_page = 1
curated_news_list = []


def get_pages():
    global current_page

    for i in range(NUMBER_OF_PAGES):
        run_scrapper()
        current_page += 1

    return sort_posts_by_votes(curated_news_list)
    # print(curated_news_list)


def sort_posts_by_votes(custom_list):
    return sorted(custom_list, key=lambda x: x["votes"], reverse=True)


def run_scrapper():

    url = f"https://news.ycombinator.com/news?p={current_page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")

    posts = soup.select(".titleline")
    links = soup.select("span.titleline > a")
    subtexts = soup.select(".subtext")

    for index, item in enumerate(posts):
        title = posts[index].getText()
        href = links[index].get(key="href", default=None)
        vote_texts = subtexts[index].select(".score")

        if len(vote_texts):
            points = int(vote_texts[0].getText().replace(" points", ""))

            if points > 99:
                curated_news_list.append({"title": title, "link": href, "votes": points})


pprint(get_pages())

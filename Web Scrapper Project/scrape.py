import requests
from bs4 import BeautifulSoup
from pprint import pprint

response = requests.get("https://news.ycombinator.com/news")
soup = BeautifulSoup(response.text, "html.parser")

response2 = requests.get("https://news.ycombinator.com/news?p=2")
soup2 = BeautifulSoup(response2.text, "html.parser")

posts = soup.select(".titleline")
links = soup.select("span.titleline > a")
subtexts = soup.select(".subtext")

posts2 = soup2.select(".titleline")
links2 = soup2.select("span.titleline > a")
subtexts2 = soup2.select(".subtext")

mega_posts = posts + posts2
mega_links = links + links2
mega_subtexts = subtexts + subtexts2


def sort_posts_by_votes(custom_list):
    return sorted(custom_list, key=lambda k: k["votes"], reverse=True)


def run_scrapper(post, link, vote):
    hot_news = []

    for index, item in enumerate(post):
        title = item.getText()
        href = link[index].get("href", None)
        vote_texts = vote[index].select(".score")

        if len(vote_texts):
            points = int(vote_texts[0].getText().replace(" points", ""))

            if points > 99:
                hot_news.append({"title": title, "link": href, "votes": points})

    return sort_posts_by_votes(hot_news)


pprint(run_scrapper(mega_posts, mega_links, mega_subtexts))

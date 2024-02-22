import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get("https://news.ycombinator.com/news")
soup = BeautifulSoup(res.text, features="html.parser")

# print(soup.body.prettify())
# posts = soup.select('.titleline')

posts = soup.findAll(name="span", attrs={"class": "titleline"})
links = soup.select("span > a")
votes = soup.findAll(name="span", attrs={"class": "score"})

# votes = soup.select('.score')

# print(posts[0])
# print(votes[0])
# print(links)

for link in links:
    print(link.get("href"))


def run_scrapper():
    hot_news = []

    for index, item in enumerate(posts):
        title = posts[index].getText()
        # href = posts[index].find_next_sibling('a').get('href', None)
        href = links[index].get("href", None)
        # points = votes[index].getText()

        hot_news.append({"title": title, "link": href})
    return hot_news


# print(run_scrapper())

import requests
from bs4 import BeautifulSoup

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')

# print(soup.body.prettify())
links = soup.select('.titleline')
votes = soup.select('.score')

# print(links[0].get('href'))
# print(votes[0])

def scrapper(links, votes):
    hot_news = []

    for index, item in enumerate(links):
        title = links[index].getText()
        href = links[index].get('href', None)
        # points = votes[index].getText()

        hot_news.append({'title': title, 'link': href})
    return hot_news

print(scrapper(links, votes))

import requests
from bs4 import BeautifulSoup
from pprint import pprint

CURRENT_PAGE = 1

url = f'https://news.ycombinator.com/news?p={CURRENT_PAGE}'

response = requests.get(url)
soup = BeautifulSoup(response.text, features='html.parser')

posts = soup.select('.titleline')
links = soup.select('span.titleline > a')
subtexts = soup.select('.subtext')

# for link in links:
#     print(link.get('href', default=None))


def sort_posts_by_votes(custom_list):
    return sorted(custom_list, key=lambda x: x['votes'], reverse=True)


def run_scrapper(post, link, vote):
    hot_news = []

    for index, item in enumerate(post):
        title = post[index].getText()
        href = link[index].get(key='href', default=None)
        vote_texts = vote[index].select('.score')

        if len(vote_texts):
            points = int(vote_texts[0].getText().replace(' points', ''))

            if points > 99:
                hot_news.append({'title': title, 'link': href, 'votes': points})

    return sort_posts_by_votes(hot_news)


pprint(run_scrapper(post=posts, link=links, vote=subtexts))

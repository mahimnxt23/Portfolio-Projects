import requests
from bs4 import BeautifulSoup
from pprint import pprint
from csv import DictWriter


NUMBER_OF_PAGES = 5  # The number of pages to scrape from...
current_page = 1  # currently scrapping page number...
curated_news_list = []  # The list of curated news items


def get_pages():
    """Scrape news from specified number of pages and return a sorted list of curated news items."""
    global current_page

    for i in range(NUMBER_OF_PAGES):
        run_scrapper()
        current_page += 1

    return sort_posts_by_votes(curated_news_list)


def sort_posts_by_votes(custom_list):
    """Sort a list of dictionaries by the value of the 'Votes' key in descending order."""
    return sorted(custom_list, key=lambda x: x["Votes"], reverse=True)


def run_scrapper():
    """Scrape news from a page and add (Title, Link, Votes) as dictionary to the curated news list."""

    url = f"https://news.ycombinator.com/news?p={current_page}"
    response = requests.get(url)
    soup = BeautifulSoup(
        response.text, features="html.parser"
    )  # Parse the response text using BeautifulSoup...

    # Select elements that contain post titles, links, and subtexts...
    posts = soup.select(".titleline")
    links = soup.select("span.titleline > a")
    subtexts = soup.select(".subtext")

    # Loop through the posts
    for index, item in enumerate(posts):
        title = posts[index].getText()
        href = links[index].get(key="href", default=None)
        vote_texts = subtexts[index].select(".score")

        if len(vote_texts):
            points = int(vote_texts[0].getText().replace(" points", ""))  # converting into an integer...

            if points > 99:  # only adding if votes are over 100...
                curated_news_list.append({"Title": title, "Link": href, "Votes": points})


def export_as_csv():
    """Export the curated news list as a csv file."""
    global curated_news_list

    # Sort the curated news list by votes to build the csv...
    sorted_news_list = sort_posts_by_votes(curated_news_list)

    # writing a csv file...
    with open("curated_news.csv", "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = DictWriter(
            csv_file, fieldnames=["Title", "Link", "Votes"]
        )  # Creating csv writer object...
        csv_writer.writeheader()  # Writing the header row...

        for news in sorted_news_list:
            csv_writer.writerow(news)  # Writing a row with the news data...

        # Printing a message to indicate the csv file is generated...
        print("\n\nGenerated the CSV file in Project Directory...")


if __name__ == "__main__":
    # get_pages()
    pprint(get_pages())  # using this to see it in terminal and save the hassle of opening a csv reader 😅...
    export_as_csv()

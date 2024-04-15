# Curated News Scraper

This is a Python script that scrapes news from Hacker News and exports them as a CSV file. The script only selects news that have more than 100 votes and sorts them by the number of votes in descending order.

## Requirements

To run this script, you need the following:

- Python 3.8 or higher
- Requests library
- BeautifulSoup library
- CSV library

## Installation

To install the required libraries, you can use pip:

```bash
pip install requests
pip install beautifulsoup4
```

## Usage

To run the script, you can use the following command:

```bash
python curated_news_scraper.py
```

The script will scrape news from 5 pages of Hacker News and print them on the terminal. It will also create a CSV file named `curated_news.csv` in the same directory as the script. The CSV file will have three columns: Title, Link, and Votes.

## Features

The script has the following features:

- It uses the Requests library to make HTTP requests to Hacker News
- It uses the BeautifulSoup library to parse the HTML response and extract the relevant data
- It uses the CSV library to write the data to a CSV file
- It uses the pprint module to format the output on the terminal
- It uses global variables to store the number of pages to scrape, the current page number, and the curated news list
- It uses functions to modularize the code and perform specific tasks
- It uses docstrings to document the functions
- It uses comments to explain the code logic
- It uses a main block to execute the script only when run directly

## License

This project is licensed under the MIT License - see the [LICENSE] file for details.


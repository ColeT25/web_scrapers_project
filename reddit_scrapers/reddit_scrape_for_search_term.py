import datetime
import time
import os
import sys

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def scrape_reddit_for_search(search_string=None) -> None:
    # todo features to add:
    # be able to do multiple searches and write them to the same file
    # be able to search other things not just titles but things like comments/communities/people
    # be able to only select results with certain terms
    """
    Search reddit for a string, and collect data on the search results in a csv file

    :param search_string: the string to search on reddit and scrape the results for
    """

    # allow for command line arguments or user input to provide the search term
    if search_string:
        search_term = search_string
    else:
        search_term = input("Enter your desired search term: ")

    # set up selenium driver
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    time.sleep(1)

    driver.get(f'https://www.reddit.com/search/?q={search_term}')

    time.sleep(5)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)

    # set up arrays to keep track of data being scrubbed
    subreddits = []
    titles = []
    upvotes = []
    comments = []
    authors = []
    awards = []

    # no new content and last_length will be used to exit the while loop when there are no
    # more search results remaining to scrub
    no_new_content = False
    last_length = len(titles)

    while not no_new_content:
        # soupify the page content
        content = driver.page_source
        page_html_soup = BeautifulSoup(content, features="html.parser")

        # loop through every div containing search results and extract relevant data
        for element in page_html_soup.find_all('div', attrs={'class': '_1poyrkZ7g36PawDueRza-J'}):
            subreddit = element.find('a', attrs={'class': '_305seOZmrgus3clHOXCmfs'}).text
            title = element.find('h3', attrs={'class': '_eYtD2XCVieq6emjKBH3m'}).text
            if subreddit in subreddits and title in titles:
                pass  # avoids repeats in data
            else:
                subreddits.append(subreddit)
                titles.append(title)

                author = element.find('a', attrs={'class': '_3-fo1J0EWS8TawiUkoZ9DH'})
                if author:
                    authors.append(author.text)
                else:
                    authors.append(element.find('span', attrs={'class': 'lizQBHVukyun2S2babj-l'}).text)

                for sub_element in element.find_all('span', attrs={'class': '_vaFo96phV6L5Hltvwcox'}):
                    current_text = sub_element.text.lower()
                    if 'upvotes' in current_text:
                        upvotes.append(current_text.replace(' upvotes', ''))
                    elif 'upvote' in current_text:
                        upvotes.append(current_text.replace(' upvote', ''))
                    elif 'comments' in current_text:
                        comments.append(current_text.replace(' comments', ''))
                    elif 'comment' in current_text:
                        comments.append(current_text.replace(' comment', ''))
                    elif 'awards' in current_text:
                        awards.append(current_text.replace(' awards', ''))
                    elif 'award' in current_text:
                        awards.append(current_text.replace(' award', ''))
                    else:
                        # throws an exception to stop everything if data starts slipping through the cracks that shouldn't
                        raise Exception(f'Something bad is happening in the below text, it must contain something it isn\'t supposed to:\n{current_text}')

        # if the titles array has not grown you know that there is no more content being added, so the while loop can terminate
        if last_length == len(titles):
            no_new_content = True
        else:
            last_length = len(titles)

        # scroll down to find more content if it exists
        driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
        time.sleep(2)

    # create a pandas DataFrame for scrapped data and write it to a csv file in scraped_data\reddit for safe keeping
    df = pd.DataFrame({'Post title': titles, 'Author': authors, 'Number of upvotes': upvotes, 'Number of awards': awards, 'Subreddit': subreddits, 'Number of comments': comments})
    os.chdir('..')
    file_name = f'scraped_data\\reddit\\redit_scrape_for_search_term--{search_term}--{datetime.date.today()}.csv'
    df.to_csv(file_name, index=False, encoding='utf-8')
    print(f'Found {last_length} search results on {search_term}, wrote results to "{file_name}"')

    driver.quit()


if __name__ == '__main__':
    # todo maybe add ability to scrape multiple pages and put the results in the same files??
    # take command line arguments if they exist
    if len(sys.argv) > 1:
        search = ''
        for arg in sys.argv:
            if arg != sys.argv[0]:
                search = f'{search} {arg}'
        scrape_reddit_for_search(search)
    else:
        scrape_reddit_for_search()

import datetime
import pytz
import time
import os
import sys
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# django takes some extra effort to get setup and imported correctly below
sys.path.append('../scraper_site')
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraper_site.settings'
import django
django.setup()
from scraperUI.models import RedditSearchResult, RedditSearchTerm
from django.utils import timezone


def convert_data_to_int(data_string: str) -> int:
    """
    Takes a data string with k or . in it and converts it into an int. EX: 3.9K becomes 3900

    :param data_string: the string with the number you would like converted to an int
    :return: The integer equivalent of the input string
    """
    if '.' in data_string:
        int_data = data_string.replace('k', '00')
    else:
        int_data = data_string.replace('k', '000')
    int_data = int_data.replace('.', '')
    return int(int_data)


def scrape_reddit_for_search(search_string=None) -> None:

    """
    Search reddit for a string, and collect data on the search results in a csv file and on a sqlite db to view using django

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
        # todo add code to scrape and store the links to reddit posts for use on django
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
    driver.quit()

    # create a pandas DataFrame for scrapped data and write it to a csv file in scraped_data\reddit for safe keeping
    df = pd.DataFrame({'Post title': titles, 'Author': authors, 'Number of upvotes': upvotes, 'Number of awards': awards, 'Subreddit': subreddits, 'Number of comments': comments})
    os.chdir('..')
    file_name = f'scraped_data\\reddit\\redit_scrape_for_search_term--{search_term}--{datetime.date.today()}.csv'
    df.to_csv(file_name, index=False, encoding='utf-8')

    # write results to sqlite db
    timezone.activate(pytz.timezone('America/Chicago'))
    current_date = timezone.localtime(timezone.now())

    new_term = RedditSearchTerm(searched_term=search_term, date_searched=current_date)
    new_term.save()
    for _, data in df.iterrows():
        upvote_int = convert_data_to_int(data['Number of upvotes'])
        comment_int = convert_data_to_int(data['Number of comments'])
        # todo add rewards and links to posts once it's in the model
        new_result = RedditSearchResult(search_term=new_term, post_title=data['Post title'], author=data['Author'],
                                        subreddit=data['Subreddit'], upvotes=upvote_int, comments=comment_int)
        new_result.save()

    print(f'Found {last_length} search results on {search_term}, wrote results to "{file_name}"')


if __name__ == '__main__':
    # take command line arguments if they exist
    if len(sys.argv) > 1:
        search = ''
        for arg in sys.argv:
            if arg != sys.argv[0]:
                search = f'{search} {arg}'
        scrape_reddit_for_search(search)
    else:
        scrape_reddit_for_search()

import datetime
import time

import pandas as pd
import re
import selenium.common.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# TODO THIS FILE IS VERY INCOMPLETE, DOESN'T WORK YET AND IS MISSING DOCUMENTATION
def create_company_data_storage(*companies):
    data_struct = {}
    for company in companies:
        data_struct[company] = {
            'market name': '',
            'current value': None,
            'market change percentage': None,
            'market change value': None,
            'previous close': None,
            'bid': None,
            'ask': None,
            '1 year target Est': None,
            'is_over_valued': None
        }
    return data_struct


def scrape_yahoo_for_stocks(*companies):
    # set up selenium driver
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()

    # set up data structures
    scraped_data = create_company_data_storage(*companies)

    for company in companies:
        driver.get('https://finance.yahoo.com/')

        time.sleep(4)
        try:
            close_modal = driver.find_element(By.CLASS_NAME, 'close')
        except selenium.common.exceptions.NoSuchElementException:
            close_modal = None

        if close_modal:
            close_modal.click()
            time.sleep(0.5)

        driver.find_element(By.NAME, 'yfin-usr-qry').send_keys(company)
        time.sleep(1)

        driver.find_element(By.ID, 'header-desktop-search-button').click()
        time.sleep(1)

        try:
            exit_login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Maybe later')]")
        except selenium.common.exceptions.NoSuchElementException:
            exit_login_button = None

        if exit_login_button:
            exit_login_button.click()
            time.sleep(0.5)

        html_soup = BeautifulSoup(driver.page_source, features='html.parser')

        # get market name
        market_name = html_soup.find('h1', attrs={'class': "D(ib)"}).text
        isolated_market_name = re.search(r'\((.*)\)', market_name).group(1)
        scraped_data[company]['market name'] = isolated_market_name

        # get current value
        # todo found wrong value, need to adjust
        scraped_data[company]['current value'] = html_soup.select(".e3b14781.f5a023e1")[0].text

        # get market change percentage and market change value
        #todo format this better, also not working yet
        scraped_data[company]['market change percentage'] = float(html_soup.select(".e3b14781.f4be3290.f5a023e1")[0].text)
        scraped_data[company]['market change value'] = float(html_soup.select(".e3b14781.f4be3290.e983cf79")[0].text)

    driver.close()


if __name__ == '__main__':
    # merely tests, this function will actually be used in a different file
    scrape_yahoo_for_stocks('apple', 'microsoft')
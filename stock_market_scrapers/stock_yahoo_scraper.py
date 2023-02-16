import datetime
import time
import os
import sys

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


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
        close_modal = driver.find_element(By.CLASS_NAME, 'close')
        if close_modal:
            close_modal.click()
            time.sleep(1)

        driver.find_element(By.NAME, 'yfin-usr-qry').send_keys(company)
        time.sleep(5)

        driver.find_element(By.ID, 'header-desktop-search-button').click()
        time.sleep(1)

    # todo sign in modal exiting not currently working
        sign_in_modal = driver.find_element(By.CLASS_NAME, 'Bxz(bb)')
        if sign_in_modal:
            sign_in_modal.find_element(By.CLASS_NAME, 'Pos(a)').click()
            time.sleep(1)

    # todo fill up data structure and add code to screenshot full screen line for looking at

    driver.close()


if __name__ == '__main__':
    # merely tests, this function will actually be used in a different file
    scrape_yahoo_for_stocks('apple', 'microsoft')
import datetime
import time
import os

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# this scraper was largely created for practice and was mostly sourced from https://www.webscrapingapi.com/python-selenium-web-scraper
# I coded this to become more familiar with the BeautifulSoup and selenium libraries before trying to do more interesting things with a web scraper
# so this isn't going to be commented or very impressive, but it is how I began learning
# there also won't be any documentation in the readme about this file

options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://www.reddit.com/r/learnprogramming/top/?t=month")

login_button = driver.find_element(By.CLASS_NAME, '_10BQ7pjWbeYP63SAPNS8Ts')
login_button.click()

driver.switch_to.frame(driver.find_element(By.CLASS_NAME,'_25r3t_lrPF3M6zD2YkWvZU'))
driver.find_element(By.ID, 'loginUsername').send_keys('CherokeePrince')
driver.find_element(By.ID, 'loginPassword').send_keys('F/cuYrrkqh5Q9<6')

driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(5)


titles = []
upvotes = []
authors = []
for i in range(20):
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")

    for element in soup.find_all('div', attrs={'class': '_1poyrkZ7g36PawDueRza-J'}):
        title = element.find('h3', attrs={'class': '_eYtD2XCVieq6emjKBH3m'})
        upvote = element.find('div', attrs={'class': '_1rZYMD_4xY3gRcSS3p8ODO'})
        author = element.find('a', attrs={'class': '_2tbHP6ZydRpjI44J3syuqC'})

        titles.append(title.text)
        upvotes.append(upvote.text)
        authors.append(author.text)

    driver.execute_script("window.scrollBy(0,1000);")
    time.sleep(0.2)

df = pd.DataFrame({'Post title': titles, 'Author': authors, 'Number of upvotes': upvotes})
os.chdir('..')
df.to_csv(f'scraped_data\\reddit\\learnprogramming_posts--{datetime.date.today()}.csv', index=False, encoding='utf-8')

driver.quit()

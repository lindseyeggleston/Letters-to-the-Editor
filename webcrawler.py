import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

_NYT_HOMEPAGE = 'https://www.nytimes.com/'


class NewYorkTimesCrawler:
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument("—-incognito")
        self.driver = webdriver.Chrome(
            executable_path="/usr/local/bin/chromedriver",
            chrome_options=option)
    
    def search(self, article_title: str):
        # get NYT homepage
        self.driver.get(_NYT_HOMEPAGE)

        # activate search button
        search_button = self.driver.find_element_by_xpath(
            "//button[@data-test-id='search-button']")
        search_button.click()
        
        # type article title
        text_area = self.driver.find_element_by_xpath(
            "//input[@name='query' and @type='text']")
        text_area.send_keys(article_title)

        # submit form
        submit_button = self.driver.find_element_by_xpath(
            "//button[@data-test-id='search-submit' and @type='submit']")
        submit_button.click()

        # select first from search results
        search_results = self.driver.find_element_by_xpath("//ol[@data-testid='search-results']")
        pass
    
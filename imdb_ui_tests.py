#!/usr/bin/env python3
from utils import get_data, get_year

import unittest
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


class SortingButtonTest(unittest.TestCase):
    """Sorting Button Test:
    Expected case: When selecting release date and clicking sorting button, it should sort movies in ascending order by release date.
    My solution: The test divided into several steps:
        * Used custom BeautifulSoup script[get_year()] and get the data from original list.
        * Getting current url as well as url arguments are updated, we [get_years()] from updated list.
        * Sorting original list of years 
        * Testing equality between original_list and current_url lists.
    """

    def setUp(self):
        self.url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250_6'
        caps = {'browserName': os.getenv('BROWSER', 'chrome')}
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=caps
        )

    def test_sorting_button_click(self):
        self.driver.get(self.url)
        select = Select(
            self.driver.find_element_by_id('lister-sort-by-options'))  # get dropdown for selecting filtering
        select.select_by_value('us:descending')  # Select Release Date filter

        sort_button = self.driver.find_element_by_xpath(
            '//*[@id="main"]/div/span/div/div/div[3]/div/div/div[1]/span')
        sort_button.click()  # click sorting button
        current_url = self.driver.current_url
        # Getting years list of current url
        current_url_years = get_year(current_url)
        data = get_year(self.url)
        data.sort(key=lambda x: int(x.replace('(', '').replace(')', '')))
        self.assertEqual(current_url_years, data,
                         'Sorting button does not work properly')

    def tearDown(self):
        self.driver.close()


class SmokeTestSearch(unittest.TestCase):
    """Smoke Test Search - Testing that Search Bar works properly:
    Expected case: When writing down a movie name in search bar and we should get movie name that matches our search.
        * search_key - Test movie name. E.g. "Inception"
        * search_bar - Searchbar that is found by xpath and got [search_key] with [.send_keys()]
        * search_button - Search Button that is found by ID and clicked by [.click()]
        * search_results - Search results by finding elements with 'result_text' class . 
        * Test if [search_key] is in [search_results_text] or not.  
    """

    def setUp(self):
        self.url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250_6'
        # self.driver = webdriver.Firefox()
        caps = {'browserName': os.getenv('BROWSER', 'chrome')}
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=caps
        )

    def test_smoke_search(self):
        self.driver.get(self.url)
        search_key = 'Inception'
        self.driver.implicitly_wait(5)
        search_bar = self.driver.find_element_by_id('suggestion-search')
        search_bar.send_keys(search_key)
        search_button = self.driver.find_element_by_id(
            'suggestion-search-button')
        search_button.click()

        search_results = self.driver.find_elements_by_class_name('result_text')

        search_results_text = ""
        for result in enumerate(search_results):
            # print(result[1].text)
            search_results_text += result[1].text
        self.assertIn(search_key, search_results_text,
                      f'Search results does not contain keyword {search_key}')

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

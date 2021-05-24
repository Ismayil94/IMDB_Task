#!/usr/bin/env python3
from utils import get_data, get_year

import unittest
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


class SortingRankingTest(unittest.TestCase):
    """Sorting Ranking Test:
    Expected case: By default Top 250 list should be sorted by rating points.
        * data - original list of movies by [get_data()]
        * ranking_sorted - sorted original list copy by rating.
        * Testing equality of 2 lists.
    """

    def setUp(self):
        self.url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250_6'
        caps = {'browserName': os.getenv('BROWSER', 'chrome')}
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=caps
        )

    def test_sorting_ranking(self):
        data = get_data(self.url)
        ranking_sorted = sorted(
            data, key=lambda item: float(item['rating']), reverse=True)
        self.assertEqual(data, ranking_sorted,
                         "Data isn't sorted by ranking in descending order.")

    def tearDown(self):
        self.driver.close()


class SortingYearTest(unittest.TestCase):
    """Sorting Year Test:
    Expected case: If we change sort by dropdown to Release Date website should sort it by year.
        * Used custom BeautifulSoup script[get_year()] and get the data from original list.
        * Getting current url as well as url arguments are updated, we [get_years()] from updated list.
        * Sorting original list of years
        * Testing equality between original_list and current_url lists
"""
    def setUp(self):
        self.url = 'https://www.imdb.com/chart/top?ref_=nv_mv_250_6'
        caps = {'browserName': os.getenv('BROWSER', 'chrome')}
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=caps
        )

    def test_sorting_year(self):
        data = get_data(self.url)
        self.driver.get(self.url)

        # get dropdown for selecting filtering
        select = Select(self.driver.find_element_by_id('lister-sort-by-options'))
        select.select_by_value('us:descending')  # Select Release Date filter
        current_url = self.driver.current_url
        # Getting years list of current url
        current_url_years = get_year(current_url)
        data = get_year(self.url)
        data.sort(key = lambda x: -int(x.replace('(', '').replace(')', '')))
        self.assertEqual(current_url_years, data,
                         'Sorting by release date does not work')

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

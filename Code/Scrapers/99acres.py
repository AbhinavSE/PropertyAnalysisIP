import os
from time import sleep
import pandas as pd
from tqdm import tqdm
from .scraper import Scraper
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class _99acres(Scraper):
    def __init__(self):
        super().__init__()
        self.index_url = "https://www.99acres.com/search/property/buy/delhi-ncr-all?city=1&preference=S&area_unit=1&res_com=R"

    def run(self):
        try:
            self.driver.maximize_window()
            self.driver.get(self.index_url)
            posts = self.get_all_posts()
            post_list = []
            try:
                self.extract(posts, post_list)
            finally:
                pd.DataFrame(post_list).to_csv(os.getcwd() + "/Data/magicbricks.csv", index=False)

        finally:
            self.driver.quit()

    def get_all_posts(self):
        # get all links with Xpath for posts under div with itemtype=//schema.org/Apartment and meta itemprop=url
        self.wait_for_element("//*[@itemtype='//schema.org/Apartment']/meta[@itemprop='url']", By.XPATH)
        self.scroll_down(times=3)
        urls = self.driver.find_elements(By.XPATH, "//*[@itemtype='//schema.org/Apartment']/meta[@itemprop='url']")
        # self.driver.get_screenshot_as_file('ss.png')
        urls = [url.get_attribute("content") for url in urls]
        print(f'Found {len(urls)} posts')
        return urls

    def extract(self, urls, post_list):
        for i, url in enumerate(urls):
            print(f'[{i+1}/{len(urls)}] Scraping {url}')
            print('--------------------------------------------------')
            try:
                post_dict = {'url': url}
                self.driver.get(url)
                sleep(2)

                self.wait_for_element('.propOverView', By.CSS_SELECTOR)
                titles = self.driver.find_elements(By.CSS_SELECTOR, '.propOverView .p_title')
                values = self.driver.find_elements(By.CSS_SELECTOR, '.propOverView .p_value')
                print(f'propOverView: {len(titles), len(values)}')
                for title, value in zip(titles, values):
                    if title != '' and title is not None:
                        post_dict[title.text] = value.text

                self.wait_for_element('#propertyDetailTabData', By.CSS_SELECTOR)
                titles = self.driver.find_elements(By.CSS_SELECTOR, "#propertyDetailTabData .p_title")
                values = self.driver.find_elements(By.CSS_SELECTOR, "#propertyDetailTabData .p_value")
                print(f'propertyDetailTabData: {len(titles), len(values)}')
                for title, value in zip(titles, values):
                    if title != '' and title is not None:
                        post_dict[title.text] = value.text

                post_list.append(post_dict)
                print()
            except Exception as e:
                print(f'Failed to scrape {url} due to: {e}')
            print(f'Posts scraped: {len(post_list)}')
        
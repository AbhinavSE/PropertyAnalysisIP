import os
from time import sleep
import pandas as pd
from tqdm import tqdm
from .scraper import Scraper
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class _99acresScraper(Scraper):
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
                pd.DataFrame(post_list).to_csv(os.getcwd() + "/Data/99acres.csv", index=False)

        finally:
            self.driver.quit()

    def get_all_posts(self):
        # get all links with Xpath for posts under div with itemtype=//schema.org/Apartment and meta itemprop=url
        urls = self.driver.find_elements(By.CSS_SELECTOR, ".srpTop__tuplesWrap section a")
        urls = [url.get_attribute('href') for url in urls if url.get_attribute('href') is not None][1:]
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
                # self.wait_for_element('#pdPrice')
                # post_dict['price'] = self.driver.find_element(By.CSS_SELECTOR, "#pdPrice").text

                self.wait_for_element('#FactTableComponent')
                titles = self.driver.find_elements(By.CSS_SELECTOR, "#FactTableComponent .component__tableHead")
                values = self.driver.find_elements(By.CSS_SELECTOR, "#FactTableComponent .component__details")
                for title, value in zip(titles, values):
                    post_dict[title.text] = value.text
                
                self.wait_for_element('.NearByLocation__infoText')
                post_dict['Nearby'] = [e.text for e in self.driver.find_elements(By.CSS_SELECTOR, '.NearByLocation__infoText') if e.text != '']

                print(*post_dict.items(), sep='\n')
                post_list.append(post_dict)
                print()
            except Exception as e:
                print(f'Failed to scrape {url} due to: {e}')
            print(f'Posts scraped: {len(post_list)}')
        
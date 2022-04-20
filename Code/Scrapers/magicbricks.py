import os
from time import sleep

import pandas as pd
from tqdm import tqdm
from .scraper import Scraper
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class MagicbricksScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.index_url = "https://www.magicbricks.com/property-for-sale-rent-in-New%20Delhi/residential-real-estate-New%20Delhi"
        self.save_location = "Data/magicbricks.csv"
    
    def get_saved_posts(self):
        df = pd.read_csv(self.save_location)
        return set(df['url'].tolist())
    
    def save_posts(self, post_list):
        df = pd.read_csv(self.save_location)
        df = df.append(post_list, ignore_index=True)
        df.reset_index(drop=True).to_csv(self.save_location, index=False)
        
    
    def search(self):
        sleep(2)
        # chosen_location_elements = self.driver.find_elements(By.CSS_SELECTOR, ".mb-search__tag")
        # for element in chosen_location_elements:
        #     close_button = element.find_element(By.CSS_SELECTOR, ".mb-search__tag-close")
        #     self.driver.execute_script("arguments[0].click();", close_button)
        
        # search_location_box = self.driver.find_element(By.CSS_SELECTOR, "#keyword")
        # search_location_box.send_keys(self.location)
        # search_location_box.send_keys(Keys.ENTER)
        self.wait_for_element(".mb-search__btn", click=True)
        search_btn = self.driver.find_element(By.CSS_SELECTOR, ".mb-search__btn")
        self.driver.execute_script("arguments[0].click();", search_btn)
        sleep(2)

    def get_all_posts(self, pages):
        # get all links with Xpath for posts under div with itemtype=//schema.org/Apartment and meta itemprop=url
        self.wait_for_element("//*[@itemtype='//schema.org/Apartment']/meta[@itemprop='url']", By.XPATH)
        self.scroll_down(times=pages)
        urls = self.driver.find_elements(By.XPATH, "//*[@itemtype='//schema.org/Apartment']/meta[@itemprop='url']")
        urls = [url.get_attribute("content") for url in urls]
        print(f'Total posts found: {len(urls)}')
        # Remove already scraped urls
        urls = [url for url in urls if url not in self.get_saved_posts()]
        print(f'Total posts left: {len(urls)}')
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
            except Exception as e:
                print(f'Failed to scrape {url} due to: {e}')
            print(f'Posts scraped: {len(post_list)}')

    def run(self, pages=10):
        try:
            self.driver.maximize_window()
            self.driver.get(self.index_url)
            self.search()
            posts = self.get_all_posts(pages)
            post_list = []
            try:
                self.extract(posts, post_list)
            finally:
                self.save_posts(post_list)

        finally:
            self.driver.quit()
        
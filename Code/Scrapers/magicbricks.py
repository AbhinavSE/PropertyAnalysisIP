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

    def get_all_posts(self):
        # get all links with Xpath for posts under div with itemtype=//schema.org/Apartment and meta itemprop=url
        self.wait_for_element("//*[@itemtype='//schema.org/Apartment']/meta[@itemprop='url']", By.XPATH)
        urls = self.driver.find_elements(By.XPATH, "//*[@itemtype='//schema.org/Apartment']/meta[@itemprop='url']")
        urls = [url.get_attribute("content") for url in urls]
        return urls

    def extract(self, urls):
        post_list = []
        for url in tqdm(urls):
            post_dict = {}
            # post_dict['url'] = post.find_element(By.XPATH, "./meta[@itemprop='url']").get_attribute("content")
            # post_dict['title'] = post.find_element(By.XPATH, "./meta[@itemprop='name']").get_attribute("content")
            # post_dict['description'] = post.find_element(By.XPATH, "./meta[@itemprop='description']").get_attribute("content")
            # post_dict['address'] = post.find_element(By.XPATH, "./meta[@itemprop='address']/meta[@itemprop='addressLocality']").get_attribute("content")
            # post_dict['number_of_rooms'] = post.find_element(By.XPATH, "./meta[@itemprop='numberOfRooms']").get_attribute("content")
            # post_dict['floor_size'] = post.find_element(By.XPATH, "./meta[@itemprop='floorSize']").get_attribute("content")
            self.driver.get(url)
            self.wait_for_element('.p_title', By.CSS_SELECTOR)
            titles = self.driver.find_elements(By.CSS_SELECTOR, '.p_title')
            values = self.driver.find_elements(By.CSS_SELECTOR, '.p_value')
            for title, value in zip(titles, values):
                post_dict[title.text] = value.text
            post_list.append(post_dict)
            # self.driver.back()
        return post_list

    def run(self):
        try:
            self.driver.maximize_window()
            self.driver.get(self.index_url)
            self.search()
            posts = self.get_all_posts()
            post_list = self.extract(posts)
            pd.DataFrame(post_list).to_csv("../Data/magicbricks.csv", index=False)

        finally:
            self.driver.quit()
        
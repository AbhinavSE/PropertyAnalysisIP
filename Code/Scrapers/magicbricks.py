from time import sleep
from .scraper import Scraper
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class MagicbricksScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.index_url = "https://www.magicbricks.com/property-for-sale-rent-in-New%20Delhi/residential-real-estate-New%20Delhi"
    
    def search(self):
        sleep(5)
        chosen_location_elements = self.driver.find_elements(By.CSS_SELECTOR, ".mb-search__tag")
        for element in chosen_location_elements:
            close_button = element.find_element(By.CSS_SELECTOR, ".mb-search__tag-close")
            self.driver.execute_script("arguments[0].click();", close_button)
        search_location_box = self.driver.find_element(By.CSS_SELECTOR, "#keyword")

        search_location_box.send_keys(self.location)
        search_location_box.send_keys(Keys.RETURN)
        self.wait_for_element(".mb-search__btn", click=True)
        search_btn = self.driver.find_element(By.CSS_SELECTOR, ".mb-search__btn")
        self.driver.execute_script("arguments[0].click();", search_btn)

    def run(self):
        try:
            self.driver.maximize_window()
            self.driver.get(self.index_url)
            self.search()
        finally:
            self.driver.quit()
        
from .scraper import Scraper
from selenium.webdriver.common.keys import Keys

class MagicbricksScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.index_url = "https://www.magicbricks.com/property-for-sale-rent-in-New%20Delhi/residential-real-estate-New%20Delhi"
    
    def search(self):
        search_location_div = self.driver.find_element_by_id("keyword_autoSuggestSelectedDiv")

        chosen_location_elements = search_location_div.find_element_by_class_name("mb-search__tag")
        for element in chosen_location_elements:
            close_button = chosen_location_elements.find_element_by_class_name("mb-search__tag-close")
            close_button.click()
        search_location_box = search_location_div.find_element_by_id("keyword")

        search_location_box.send_keys(self.location)
        search_location_box.send_keys(Keys.RETURN)

    def run(self):
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.search()
        
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Scraper:
    def __init__(self):
        MagicBricksURL = "https://www.magicbricks.com/property-for-sale-rent-in-New%20Delhi/residential-real-estate-New%20Delhi"
        Location = "New Delhi"

        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(MagicBricksURL)

        search_location_div = driver.find_element_by_id("keyword_autoSuggestSelectedDiv")

        chosen_location_elements = search_location_div.find_element_by_class_name("mb-search__tag")
        for element in chosen_location_elements:
            close_button = chosen_location_elements.find_element_by_class_name("mb-search__tag-close")
            close_button.click()
        search_location_box = search_location_div.find_element_by_id("keyword")

        search_location_box.send_keys(Location)
        search_location_box.send_keys(Keys.RETURN)

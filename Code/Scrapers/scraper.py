# Imports
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException


class Scraper:
    def __init__(self):
        self.location = "New Delhi"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=1440,900")
        self.driver = webdriver.Chrome(executable_path="/Users/macbookpro/chromedriver/chromedriver", options=options)

    def wait_for_element(self, select: str, by=By.CSS_SELECTOR, click=False, delay=10) -> bool:
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
            if click:
                element_present = EC.element_to_be_clickable((by, select))
                WebDriverWait(self.driver, delay, ignored_exceptions=ignored_exceptions).until(element_present)
            else:
                element_present = EC.presence_of_element_located((by, select))
                WebDriverWait(self.driver, delay, ignored_exceptions=ignored_exceptions).until(element_present)
        except TimeoutException:
            print(f"Timed out waiting for element {select}")
            return False
        return True

    def scroll_down(self, times=1, delay=2):
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        for _ in range(times):
            print('Scrolling')
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(delay)
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def search(self):
        pass

# Imports
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Scraper:
    def __init__(self):
        self.location = "New Delhi"
        self.driver = webdriver.Chrome(executable_path=os.getcwd() + "/chromedriver")

    def wait_for_element(self, select: str, by=By.CSS_SELECTOR, click=False, delay=10) -> bool:
        try:
            if click:
                element_present = EC.element_to_be_clickable((by, select))
                WebDriverWait(self.driver, delay).until(element_present)
            else:
                element_present = EC.presence_of_element_located((by, select))
                WebDriverWait(self.driver, delay).until(element_present)
        except TimeoutException:
            print("Timed out waiting for element")
            return False
        return True

    def search(self):
        pass

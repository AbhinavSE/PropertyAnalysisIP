import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Scraper:
    def __init__(self):
        self.location = "New Delhi"
        self.driver = webdriver.Chrome(executable_path=os.getcwd() + "/chromedriver")

    def search(self):
        pass

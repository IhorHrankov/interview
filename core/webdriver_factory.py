"""
@package base
WebDriver Factory class implementation
It creates a web-driver instance based on browser configurations
"""
from selenium import webdriver
import os
from ..config import read_config as rd
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class WebDriverFactory:

    def __init__(self):
        self.baseUrl = rd.get_config("base_url")

    def get_driver(self):

        location = os.path.abspath(__file__ + "/../../drivers/chromedriver")
        print(location)
        os.environ["webdriver.chrome.driver"] = location
        capabilities = DesiredCapabilities.CHROME
        capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}
        capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
        driver = webdriver.Chrome(location, desired_capabilities=capabilities)

        driver.implicitly_wait(45)
        driver.maximize_window()
        driver.get(self.baseUrl)

        return driver

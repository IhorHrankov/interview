from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from ..utils import logger as cl
import logging
import time
import os
import allure


class InitDriver:
    log = cl.Logger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def take_screenshot(self, message):
        file_name = message + "." + str(round(time.time() * 1000)) + ".png"
        if len(file_name) >= 200:
            file_name = str(round(time.time() * 1000)) + ".png"
        screenshot_dir = "../screenshots/"
        relative_name = screenshot_dir + file_name
        current_dir = os.path.dirname(__file__)
        destination_file = os.path.join(current_dir, relative_name)
        destination_dir = os.path.join(current_dir, screenshot_dir)

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        self.driver.save_screenshot(destination_file)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name=file_name,
                      attachment_type=allure.attachment_type.PNG)

        self.log.info("Screenshot saved to directory: " + destination_file)

    def get_title(self):
        return self.driver.title

    def get_by_type(self, locator_type):
        locator_type = locator_type.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type" + locator_type + "passed in wrong format")
        return False

    def select_element_from_dropdown(self, locator, locator_type="id", selector="", selector_type="value"):
        try:
            element = self.get_element(locator, locator_type)
            sel = Select(element)
            if selector_type == "value":
                sel.select_by_value(selector)
                time.sleep(1)
            elif selector_type == "index":
                sel.select_by_index(selector)
                time.sleep(1)
            elif selector_type == "text":
                sel.select_by_visible_text(selector)
                time.sleep(1)
            self.log.info("Element selected with selector: " + str(selector) +
                          " and selector_type: " + selector_type)

        except:
            self.log.error("Element not selected with selector: " + str(selector) +
                           " and selector_type: " + selector_type)
            print_stack()

    def get_element(self, locator, locator_type="id"):
        element = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, locator)
            self.log.info("Element found with locator: " + locator +
                          " and locator_type: " + locator_type)
        except:
            self.log.error("Element not found with locator: " + locator +
                           " and locator_type: " + locator_type)
        return element

    def is_element_selected(self, locator, locator_type):
        is_selected = None
        try:
            element = self.get_element(locator, locator_type)
            is_selected = element.is_selected()
            self.log.info("Element found with locator: " + locator +
                          " and locator_type: " + locator_type)
        except:
            self.log.error("Element not found with locator: " + locator +
                           " and locator_type: " + locator_type)

        return is_selected

    def get_elements(self, locator, locator_type="id"):

        element = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_elements(by_type, locator)
            self.log.info("Element list found with locator: " + locator +
                          " and locator_type: " + locator_type)
        except:
            self.log.error("Element list not found with locator: " + locator +
                           " and locator_type: " + locator_type)

        return element

    def click_element(self, locator="", locator_type="id", element=None):
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.click()
            self.log.info("clicked on element with locator: " + locator +
                          " locator_type: " + locator_type)
        except:
            self.log.error("cannot click on the element with locator: " + locator +
                           " locator_type: " + locator_type)
            print_stack()

    def hover_on_element(self, locator="", locator_type="id", element=None):

        try:
            if locator:
                element = self.get_element(locator, locator_type)
            hover = ActionChains(self.driver).move_to_element(element)
            hover.perform()
            time.sleep(2)
            self.log.info("hover to element with locator: " + locator +
                          " locator_type: " + locator_type)
        except:
            self.log.error("cannot hover to the element with locator: " + locator +
                           " locator_type: " + locator_type)
            print_stack()

    def send_text(self, data, locator="", locator_type="id", element=None):
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.send_keys(data)
            self.log.info("send data on element with locator: " + locator +
                          " locator_type: " + locator_type)
        except:
            self.log.error("cannot send data on the element with locator: " + locator +
                           " locator_type: " + locator_type)
            print_stack()

    def clear_text(self, locator="", locator_type="id", element=None):
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.clear()
            self.log.info("Clear data of element with locator: " + locator +
                          " locator_type: " + locator_type)
        except:
            self.log.error("cannot clear data of the element with locator: " + locator +
                           " locator_type: " + locator_type)
            print_stack()

    def get_text(self, locator="", locator_type="id", element=None, info=""):
        try:
            if locator:
                self.log.debug("In locator condition")
                element = self.get_element(locator, locator_type)
            self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding element, size is: " + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element :: " + info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def is_element_present(self, locator="", locator_type="id", element=None):
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            if element is not None:
                self.log.info("Element found with locator: " + locator +
                              " and locator_type: " + locator_type)
                return True
            else:
                self.log.error("Element not found with locator: " + locator +
                               " and locator_type: " + locator_type)
                return False
        except:
            self.log.error("Element not found with locator: " + locator +
                           " and locator_type: " + locator_type)
            return False

    def is_element_displayed(self, locator="", locator_type="id", element=None):
        is_displayed = False
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            if element is not None:
                is_displayed = element.is_displayed()
                self.log.info("Element is displayed: " + locator +
                              " and locator_type: " + locator_type)
            else:
                self.log.error("Element is not displayed: " + locator +
                               " and locator_type: " + locator_type)
            return is_displayed
        except:
            self.log.error("Element is not displayed: " + locator +
                           " and locator_type: " + locator_type)
            return False

    def wait_for_element_clickable(self, locator, locator_type='id', timeout=20, poll_frequency=0.5):
        element = None
        try:
            self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element to be clickable")

            wait = WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            by_type = self.get_by_type(locator_type)
            element = wait.until(EC.element_to_be_clickable((by_type, locator)))

            self.log.info("Element found")
        except:
            self.log.info("Element not found")
            print_stack()

        return element

    def wait_for_element_visible(self, locator, locator_type='id', timeout=20, poll_frequency=0.5):
        element = None
        try:
            self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element to be visible")

            wait = WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            by_type = self.get_by_type(locator_type)
            element = wait.until(EC.visibility_of_element_located((by_type, locator)))

            self.log.info("Element found")
        except:
            self.log.info("Element not found")
            print_stack()

        return element

    def get_url(self):
        current_url = self.driver.current_url
        return current_url

    def go_back(self):
        self.driver.execute_script("window.history.go(-1)")

    def get_attribute_value(self, locator="", locator_type="id", element=None, attribute=""):
        try:
            if locator:
                self.log.debug("In locator condition")
                element = self.get_element(locator, locator_type)
            attribute_value = element.get_attribute(attribute)
        except:
            self.log.error("Failed to get " + attribute + " in element with locator: " +
                           locator + " and locator_type: " + locator_type)
            print_stack()
            attribute_value = None
        return attribute_value

    def refresh(self):
        self.driver.get(self.driver.current_url)

    def page_has_loaded(self):
        try:
            WebDriverWait(self.driver, 1000, poll_frequency=0.5).until(
                lambda driver: self.driver.execute_script('return document.readyState == "complete";'))
            WebDriverWait(self.driver, 1000, poll_frequency=0.5).until(
                lambda driver: self.driver.execute_script('return angular.element(document).injector().get("$http").'
                                                          'pendingRequests.length === 0'))
        except:
            return False

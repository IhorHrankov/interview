from ..utils import logger as cl
from ..config import read_config as rd
import logging
import allure
from ..core.base_page import BasePage


class LoginPage(BasePage):

    log = cl.Logger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.login_locators = self.get_page_locators('LoginPage', 'login_elements.json')

    @allure.step("opening login page")
    def open_login_page(self):
        self.driver.get(rd.get_config('base_url') + '/login')

    @allure.step("verifying successful login with valid credentials")
    def login(self, email, password):
        self.page_has_loaded()
        self.send_text(email, *self.locator(self.login_locators, 'email_field'))
        self.send_text(password, *self.locator(self.login_locators, 'password_field'))
        self.click_element(*self.locator(self.login_locators, 'login_btn'))

    def is_logged_in(self):
        return self.get_element(*self.locator(self.login_locators, 'menu_icon')).is_displayed() == True
from ..core.webdriver_factory import WebDriverFactory
from ..utils import logger as cl
import logging
import os
import allure
import time
import pytest
import json


@pytest.fixture()
def set_up():
    print("Running method level setUp")
    yield
    print("Running method level tearDown")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="function", autouse=True)
def one_time_set_up(request):
    print("Running class setUp")
    wdf = WebDriverFactory()
    driver = wdf.get_driver()

    if request.cls is not None:
        request.cls.driver = driver

    yield driver

    if request.node.rep_call.failed:
        screenshot_on_failure(driver)
        get_browser_logs_errors(driver)

    driver.quit()
    print("Running class tearDown")


def screenshot_on_failure(driver):
    try:
        file_name = "screenshot" + str(round(time.time() * 1000)) + ".png"
        if len(file_name) >= 200:
            file_name = str(round(time.time() * 1000)) + ".png"
        screenshot_dir = "../screenshots/"
        relative_name = screenshot_dir + file_name
        current_dir = os.path.dirname(__file__)
        destination_file = os.path.join(current_dir, relative_name)
        destination_dir = os.path.join(current_dir, screenshot_dir)

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        driver.save_screenshot(destination_file)
        allure.attach(driver.get_screenshot_as_png(),
                      name=file_name,
                      attachment_type=allure.attachment_type.PNG)
    except:
        pass


def get_browser_logs_errors(driver):
    log = cl.Logger(logging.DEBUG)
    code_500 = 0
    code_400 = 0
    code_401 = 0
    code_403 = 0
    code_404 = 0
    code_502 = 0
    code_503 = 0
    code_504 = 0

    #code_200 = 0

    try:
        for entry in driver.get_log('performance'):
            message = json.loads(entry['message'])
            message_string = str(message['message'])

            # if "'status': 200" in message_string:
            #     code_200 += 1
            #     log.info("Detected status 200 in response: " + message_string)
            if "'status': 400" in message_string:
                code_400 += 1
                log.info("Detected status 400 in response: " + message_string)
            elif "'status': 500" in message_string:
                code_500 += 1
                log.info("Detected status 500 in response: " + message_string)
            elif "'status': 401" in message_string:
                code_401 += 1
                log.info("Detected status 401 in response: " + message_string)
            elif "'status': 403" in message_string:
                code_403 += 1
                log.info("Detected status 403 in response: " + message_string)
            elif "'status': 404" in message_string:
                code_404 += 1
                log.info("Detected status 404 in response: " + message_string)
            elif "'status': 502" in message_string:
                code_502 += 1
                log.info("Detected status 502 in response: " + message_string)
            elif "'status': 503" in message_string:
                code_503 += 1
                log.info("Detected status 503 in response: " + message_string)
            elif "'status': 504" in message_string:
                code_504 += 1
                log.info("Detected status 503 in response: " + message_string)
    except:
        pass

    log.info("Total responses with code 400: {}, with code 500: {}, with code 401: {}, with code 403: {},"
             " with code 404: {}, with code 502: {}, with code 503: {}, with code 504: {}"
             .format(code_400, code_500, code_401, code_403, code_404, code_502, code_503, code_504))

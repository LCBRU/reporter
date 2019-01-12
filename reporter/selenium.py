"""Selenium grid connection manager
"""
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SeleniumGrid():
    """Selenium grid connection manager
    """

    CHROME = DesiredCapabilities.CHROME
    FIREFOX = DesiredCapabilities.FIREFOX

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        SELENIUM_HOST = os.environ.get("SELENIUM_HOST", '')
        SELENIUM_PORT = os.environ.get("SELENIUM_PORT", '4444')

        command_executor = 'http://{}:{}/wd/hub'.format(SELENIUM_HOST, SELENIUM_PORT)

        self.driver = webdriver.Remote(
            command_executor=command_executor,
            desired_capabilities=self.browser
        )
        self.driver.implicitly_wait(10)
        return self.driver

    def __exit__(self, *args):
        self.driver.quit()

#!/usr/bin/env python3

import os
import urllib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from reporter.core import Report
from reporter.reports.selenium import SeleniumGrid


class RedcapWebDataQuality(Report):

    PAGE_URL = 'DataQuality/index.php?pid={}'
    REDCAP_USERNAME = os.environ["REDCAP_USERNAME"]
    REDCAP_PASSWORD = os.environ["REDCAP_PASSWORD"]

    def __init__(
        self,
        redcap_instance,
        project_id,
        recipients,
        schedule=None
    ):
        self._redcap_instance = redcap_instance
        self._project_id = project_id

        super().__init__(
            introduction="The following data quality errors "
                         "were found in REDCap",
            recipients=recipients,
            schedule=schedule,
        )

    def get_report(self):

        reports = [
            {
                'message': 'Missing Required Fields',
                'div': '6'
            },
            {
                'message': 'Invalid Data Type',
                'div': '4'
            },
            {
                'message': 'Out of Range',
                'div': '9'
            },
            {
                'message': 'Hidden fields that contain values',
                'div': '7'
            },
            {
                'message': 'Invalid Multiple Fields',
                'div': '8'
            },
            {
                'message': 'Incorrect Calculated Fields',
                'div': '10'
            },
        ]

        with SeleniumGrid(SeleniumGrid.CHROME) as driver:

            self.login(driver)

            dq_page_url = urllib.parse.urljoin(
                self._redcap_instance()['base_url'],
                self.PAGE_URL.format(self._project_id),
            )

            driver.get(dq_page_url)

            driver.save_screenshot('screenshot.png')

            questionnaire_name = driver.find_element_by_id(
                "subheaderDiv2"
            ).text

            for r in reports:
                r['errors'] = self.get_count(
                    driver,
                    'ruleexe_pd-{}'.format(r['div'])
                )

        errors = ''

        for r in [r for r in reports if r['errors'] != '0']:
            errors += '- {}: {}\r\n\r\n'.format(
                r['message'],
                r['errors']
            )

        if errors:
            markdown = (
                self.get_introduction() +
                "***[{}]({})***\r\n\r\n".format(
                    questionnaire_name,
                    dq_page_url,
                ) +
                errors
            )

            return markdown, 1, None
        else:
            return '', 0, None

    def login(self, driver):
        driver.get(self._redcap_instance()['base_url'])

        username = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((
                By.NAME, "username"))
        )

        password = driver.find_element_by_name('password')

        username.send_keys(self.REDCAP_USERNAME)
        password.send_keys(self.REDCAP_PASSWORD + Keys.RETURN)

    def get_count(self, driver, identifier):
            driver.find_element_by_xpath(
                "//div[@id='{}']/button".format(identifier)
            ).click()

            return driver.find_element_by_xpath(
                "//div[@id='{}']/div[1]".format(identifier)
            ).text

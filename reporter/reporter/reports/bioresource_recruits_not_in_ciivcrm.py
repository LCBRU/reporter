#!/usr/bin/env python3

import schedule
import os
import datetime
import logging
from reporter import get_report_db, send_markdown_email, send_markdown_slack


REPORT_NAME = 'Bioresource Recruits not in CiviCRM';
RECIPIENT = os.environ["BIORESOURCE_RECRUITS_NOT_IN_CIVICRM_RECIPIENT"]
CIVICRM_SEARCH_URL = os.environ["CIVICRM_SEARCH_URL"]


def job():

    markdown = ''

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
                SELECT  bioresource_id
                FROM    CIVICRM_ScheduledReports_Bioresource_RecruitsNotInCiviCrm
                ORDER BY bioresource_id
                    ''')

            markdown = f'**{REPORT_NAME}**\r\n\r\n'
            markdown += "_The following participants have a record in REDCap, but do not have a record in CiviCRM_:\r\n\r\n"

            for row in cursor:
                markdown += f'- [{row["bioresource_id"]}]({CIVICRM_SEARCH_URL}{row["bioresource_id"]})\r\n'

            markdown += f"\r\n\r\n{cursor.rowcount} Record(s) Found"

            if cursor.rowcount > 0:
                send_markdown_email(REPORT_NAME, RECIPIENT, markdown)
                send_markdown_slack(REPORT_NAME, markdown)


schedule.every().hour.do(job)

logging.info(f"{REPORT_NAME} Loaded")

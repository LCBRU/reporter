#!/usr/bin/env python3

import schedule
import os
import datetime
import logging
from reporter import get_report_db, send_markdown_email, send_markdown_slack


REPORT_NAME = 'Bioresource Recruits not in REDCap';
RECIPIENT = os.environ["BIORESOURCE_RECRUITS_NOT_IN_REDCAP_RECIPIENT"]
CIVICRM_SEARCH_URL = os.environ["CIVICRM_SEARCH_URL"]


def job():

    markdown = ''

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
                SELECT  bioresource_id,
                        consent_date
                FROM    CIVICRM_ScheduledReports_Bioresource_RecruitsNotInRedcap
                ORDER BY consent_date, bioresource_id
                    ''')

            markdown = f'**{REPORT_NAME}**\r\n\r\n'
            markdown += "_The following participants have a record in CiviCRM, but do not have a record in REDCap_:\r\n\r\n"

            for row in cursor:
                consent_date = f'{row["consent_date"]:%d-%b-%Y}' if row['consent_date'] else ''
                markdown += f'- [{row["bioresource_id"]}]({CIVICRM_SEARCH_URL}{row["bioresource_id"]}) {consent_date}\r\n'

            markdown += f"\r\n\r\n{cursor.rowcount} Record(s) Found"

            if cursor.rowcount > 0:
                send_markdown_email(REPORT_NAME, RECIPIENT, markdown)
                send_markdown_slack(REPORT_NAME, markdown)


schedule.every().hour.do(job)

logging.info(f"{REPORT_NAME} Loaded")

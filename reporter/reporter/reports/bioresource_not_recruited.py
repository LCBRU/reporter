#!/usr/bin/env python3

import schedule
import os
import datetime
import logging
from reporter import get_report_db, send_markdown_email, send_markdown_slack


REPORT_NAME = 'Bioresource Not Recruited'
RECIPIENT = os.environ["BIORESOURCE_NOT_RECRUITED_RECIPIENT"]
CIVICRM_SEARCH_URL = os.environ["CIVICRM_SEARCH_URL"]


def bioresource_not_recruited():

    markdown = ''

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
                        SELECT bioresource_id,
                               consent_date
                        FROM CIVICRM_ScheduledReports_Bioresource_NotRecruited
                        ORDER BY consent_date, bioresource_id
                    ''')

            markdown = f'**{REPORT_NAME}**\r\n\r\n'
            markdown += ("_The following participants appear "
                         "to have full consent, but do not have a status "
                         "of recruited in CiviCRM_:\r\n\r\n")

            for row in cursor:
                consent_date = (f'{row["consent_date"]:%d-%b-%Y}'
                                if row['consent_date'] else '')
                markdown += (f'- [{row["bioresource_id"]}]'
                             f'({CIVICRM_SEARCH_URL}{row["bioresource_id"]}) '
                             f'{consent_date}\r\n')

            markdown += f"\r\n\r\n{cursor.rowcount} Record(s) Found"

            if cursor.rowcount > 0:
                send_markdown_email(REPORT_NAME, RECIPIENT, markdown)
                send_markdown_slack(REPORT_NAME, markdown)


schedule.every().monday.at("08:00").do(bioresource_not_recruited)


logging.info(f"{REPORT_NAME} Loaded")

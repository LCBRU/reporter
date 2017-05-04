#!/usr/bin/env python3

import schedule
import os
import datetime
import logging
from reporter import get_report_db, send_markdown_email, send_markdown_slack, get_recipient


REPORT_NAME = 'Bioresource Recruits not in CiviCRM'
CIVICRM_SEARCH_URL = os.environ["CIVICRM_SEARCH_URL"]


def bioresource_not_in_civicrm():

    markdown = ''

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
                SELECT  bioresource_id
                FROM CIVICRM_ScheduledReports_Bioresource_RecruitsNotInCiviCrm
                ORDER BY bioresource_id
                    ''')

            if cursor.rowcount == 0:
                return

            markdown = f'**{REPORT_NAME}**\r\n\r\n'
            markdown += ("_The following participants have "
                         "a record in REDCap, but do not have "
                         "a record in CiviCRM_:\r\n\r\n")

            for row in cursor:
                markdown += (f'- [{row["bioresource_id"]}]'
                             f'({CIVICRM_SEARCH_URL}{row["bioresource_id"]})'
                             f'\r\n')

            markdown += f"\r\n\r\n{cursor.rowcount + 1} Record(s) Found"

            send_markdown_email(
                REPORT_NAME,
                get_recipient("BIORESOURCE_RECRUITS_NOT_IN_CIVICRM_RECIPIENT"),
                markdown)
            send_markdown_slack(REPORT_NAME, markdown)


# bioresource_not_in_civicrm()
schedule.every().monday.at("08:00").do(bioresource_not_in_civicrm)

logging.info(f"{REPORT_NAME} Loaded")

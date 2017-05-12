#!/usr/bin/env python3

import schedule
import os
import datetime
import logging
from reporter import get_report_db, send_markdown_email, send_markdown_slack, get_recipient


REPORT_NAME = 'Bioresource Recruits without full consent'
CIVICRM_SEARCH_URL = os.environ["CIVICRM_SEARCH_URL"]


def bioresource_without_full_consent():

    markdown = ''

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
                SELECT  bioresource_id,
                        consent_date
                FROM    CIVICRM_ScheduledReports_Bioresource_WithoutFullConsent
                ORDER BY bioresource_id
                    ''')

            if cursor.rowcount == 0:
                return

            markdown = f'**{REPORT_NAME}**\r\n\r\n'
            markdown += ("_The following participants are recruited, "
                         "duplicates or withdrawn "
                         "in CiviCRM, but a record of full consent "
                         "cannot be found_:\r\n\r\n")

            for row in cursor:
                consent_date = (f'{row["consent_date"]:%d-%b-%Y}'
                                if row['consent_date'] else '')
                markdown += (f'- [{row["bioresource_id"]}]'
                             f'({CIVICRM_SEARCH_URL}{row["bioresource_id"]}) '
                             f'{consent_date}\r\n')

            markdown += f"\r\n\r\n{cursor.rowcount + 1} Record(s) Found"

            send_markdown_email(
                REPORT_NAME,
                get_recipient("BIORESOURCE_WITHOUT_FULL_CONSENT_RECIPIENT"),
                markdown)
            send_markdown_slack(REPORT_NAME, markdown)


# bioresource_without_full_consent()

schedule.every().monday.at("08:00").do(bioresource_without_full_consent)

logging.info(f"{REPORT_NAME} Loaded")

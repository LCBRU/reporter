#!/usr/bin/env python3

import schedule
import os
import datetime
import logging
from reporter import (get_report_db, send_markdown_email,
                      send_markdown_slack, get_recipient, get_contact_link)


REPORT_NAME = 'Bioresource Contact with Multiple Recruitments'


def bioresource_contact_multiple_recruited():

    markdown = ''

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
                    SELECT civicrm_contact_id
                    FROM i2b2_app03_bioresource_Data.dbo.LOAD_COMBINED_VALID_RECRUITED
                    GROUP BY civicrm_contact_id
                    HAVING COUNT(*) > 1
                ''')

            if cursor.rowcount == 0:
                return

            markdown = f'**{REPORT_NAME}**\r\n\r\n'
            markdown += ("_The following participants has multiple "
                         "recruited enrolments"
                         "_:\r\n\r\n")

            for row in cursor:
                markdown += '- {}\r\n\r\n'.format(get_contact_link(
                    'Click to View',
                    row["civicrm_contact_id"]))

            markdown += f"\r\n\r\n{cursor.rowcount + 1} Record(s) Found"

            send_markdown_email(
                REPORT_NAME,
                get_recipient("BIORESOURCE_BLANK_STUDY_ID_RECIPIENT"),
                markdown)
            send_markdown_slack(REPORT_NAME, markdown)


bioresource_contact_multiple_recruited()
schedule.every().monday.at("08:00").do(bioresource_contact_multiple_recruited)


logging.info(f"{REPORT_NAME} Loaded")

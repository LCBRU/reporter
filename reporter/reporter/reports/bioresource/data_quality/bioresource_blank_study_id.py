#!/usr/bin/env python3

import schedule
import os
import datetime
import logging
from reporter import (get_report_db, send_markdown_email,
                      send_markdown_slack, get_recipient, get_case_link)


REPORT_NAME = 'Bioresource Blank Study ID'


def bioresource_blank_study_id():

    markdown = ''

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
                SELECT civicrm_case_id, civicrm_contact_id
                FROM CIVICRM_ScheduledReports_Bioresource_StudyIdBlank
                ''')

            if cursor.rowcount == 0:
                return

            markdown = f'**{REPORT_NAME}**\r\n\r\n'
            markdown += ("_The following participants have a blank "
                         "study ID in the CiviCRM Study Enrolment "
                         "_:\r\n\r\n")

            for row in cursor:
                markdown += '- {}\r\n\r\n'.format(get_case_link(
                    'Click to View',
                    row["civicrm_case_id"],
                    row["civicrm_contact_id"]))

            markdown += f"\r\n\r\n{cursor.rowcount + 1} Record(s) Found"

            send_markdown_email(
                REPORT_NAME,
                get_recipient("BIORESOURCE_BLANK_STUDY_ID_RECIPIENT"),
                markdown)
            send_markdown_slack(REPORT_NAME, markdown)


# bioresource_blank_study_id()
schedule.every().monday.at("08:00").do(bioresource_blank_study_id)


logging.info(f"{REPORT_NAME} Loaded")
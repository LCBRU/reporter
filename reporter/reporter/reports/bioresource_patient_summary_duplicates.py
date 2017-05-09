#!/usr/bin/env python3

import schedule
import os
import datetime
import logging
from reporter import (get_report_db, send_markdown_email,
                      send_markdown_slack, get_recipient)


REPORT_NAME = 'Bioresource Patient Summary Duplicates'


def bioresource_patient_summary_duplicates():

    markdown = ''

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
                SELECT patient_num, COUNT(*) AS ct
                FROM    i2b2_app03_bioresource_Data.dbo.PatientSummary
                GROUP BY patient_num
                HAVING COUNT(*) > 1;
                ''')

            if cursor.rowcount == 0:
                return

            markdown = f'**{REPORT_NAME}**\r\n\r\n'
            markdown += ("_The following participants are duplicated "
                         "in the bioresource patient_summary view "
                         "_:\r\n\r\n")

            for row in cursor:
                markdown += '- {}\r\n'.format(row['patient_num'])

            markdown += f"\r\n\r\n{cursor.rowcount + 1} Record(s) Found"

            send_markdown_email(
                REPORT_NAME,
                get_recipient("BIORESOURCE_BLANK_STUDY_ID_RECIPIENT"),
                markdown)
            send_markdown_slack(REPORT_NAME, markdown)


# bioresource_patient_summary_duplicates()
schedule.every().monday.at("08:00").do(bioresource_patient_summary_duplicates)


logging.info(f"{REPORT_NAME} Loaded")

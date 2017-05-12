#!/usr/bin/env python3

import schedule
import logging
from reporter import (get_report_db, send_markdown_email,
                      send_markdown_slack, get_recipient)


REPORT_NAME = 'Bioresource Study ID Duplicates'


def bioresource_study_id_duplicates():

    markdown = ''

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
                SELECT PATIENT_IDE, PATIENT_IDE_SOURCE, COUNT(*) AS ct
                FROM i2b2_app03_bioresource_Data.dbo.Patient_Mapping pm
                GROUP BY PATIENT_IDE, PATIENT_IDE_SOURCE
                HAVING COUNT(*) > 1;
                ''')

            if cursor.rowcount == 0:
                return

            markdown = '**{}**\r\n\r\n'.format(REPORT_NAME)
            markdown += ("_The following study IDs are duplicated"
                         "_:\r\n\r\n")

            for row in cursor:
                markdown += '- {} (ID type = \'{}\')\r\n'.format(
                    row['PATIENT_IDE'],
                    row['PATIENT_IDE_SOURCE']
                )

            markdown += "\r\n\r\n{} Record(s) Found".format(
                cursor.rowcount + 1
            )

            send_markdown_email(
                REPORT_NAME,
                get_recipient("BIORESOURCE_BLANK_STUDY_ID_RECIPIENT"),
                markdown)
            send_markdown_slack(REPORT_NAME, markdown)


# bioresource_study_id_duplicates()
schedule.every().monday.at("08:00").do(bioresource_study_id_duplicates)


logging.info("{} Loaded".format(REPORT_NAME))

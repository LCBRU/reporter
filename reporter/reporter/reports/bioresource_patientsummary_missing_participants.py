#!/usr/bin/env python3

import schedule
import logging
from reporter import (get_report_db, send_markdown_email,
                      send_markdown_slack, get_recipient)


REPORT_NAME = 'Bioresource PatientSummary Missing Participants'


def bioresource_patientsummary_missing_participants():

    markdown = ''

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
                SELECT pd.Patient_Num
                FROM i2b2_app03_bioresource_Data.dbo.Patient_Dimension pd
                WHERE pd.Patient_Num NOT IN (
                    SELECT ps.Patient_Num
                    FROM i2b2_app03_bioresource_Data.dbo.PatientSummary ps)
                ''')

            if cursor.rowcount == 0:
                return

            markdown = '**{}**\r\n\r\n'.format(REPORT_NAME)
            markdown += ("_The following participants are "
                         "missing from the patient summary"
                         "_:\r\n\r\n")

            for row in cursor:
                markdown += '- {}\r\n'.format(
                    row['patient_num']
                )

            markdown += "\r\n\r\n{} Record(s) Found".format(
                cursor.rowcount + 1
            )

            send_markdown_email(
                REPORT_NAME,
                get_recipient("BIORESOURCE_BLANK_STUDY_ID_RECIPIENT"),
                markdown)
            send_markdown_slack(REPORT_NAME, markdown)


bioresource_patientsummary_missing_participants()

schedule.every().monday.at("08:00").do(
    bioresource_patientsummary_missing_participants)


logging.info("{} Loaded".format(REPORT_NAME))

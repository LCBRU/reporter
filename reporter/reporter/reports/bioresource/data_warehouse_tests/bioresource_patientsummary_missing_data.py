#!/usr/bin/env python3

import schedule
import logging
from reporter import (get_report_db, send_markdown_email,
                      send_markdown_slack, get_recipient)


REPORT_NAME = 'Bioresource PatientSummary Missing Data'
FIELDS = ['CiviCrmId', 'NhsNumber', 'UhlSystemNumber', 'BioresourceId',
          'StudyNumber', 'EnrolmentDate', 'ConsentDate', 'Gender', 'DOB',
          'DateOfBirth', 'Height', 'Weight']


def bioresource_patient_summary_missing_data():

    markdown = ''
    rec_count = 0

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            for f in FIELDS:

                cursor.execute('''
                    SELECT patient_num
                    FROM i2b2_app03_bioresource_Data.dbo.PatientSummary ps
                    WHERE ps.{} IS NULL
                    '''.format(f))

                for row in cursor:
                    rec_count += 1
                    markdown += '- {}: {} missing\r\n'.format(
                        row['patient_num'], f)

            if markdown == '':
                return

            heading = '**{}**\r\n\r\n'.format(REPORT_NAME)
            heading += ("_The following participants have "
                        "data missing from the PatientSummary"
                        "_:\r\n\r\n")

            markdown = heading + markdown

            markdown += "\r\n\r\n{} Record(s) Found".format(
                rec_count
            )

            send_markdown_email(
                REPORT_NAME,
                get_recipient("BIORESOURCE_BLANK_STUDY_ID_RECIPIENT"),
                markdown)
            send_markdown_slack(REPORT_NAME, markdown)


# bioresource_patient_summary_missing_data()

schedule.every().monday.at("08:00").do(
    bioresource_patient_summary_missing_data)


logging.info("{} Loaded".format(REPORT_NAME))

#!/usr/bin/env python3

import schedule
import os
import datetime
import logging
from reporter import (get_report_db, send_markdown_email,
                      send_markdown_slack, get_recipient, get_case_link)


REPORT_NAME = 'Bioresource Legacy ID Duplicates'


def bioresource_legacy_id_duplicates():

    markdown = ''

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
                SELECT
                    bioresource_id,
                    legacy_bioresource_id,
                    civicrm_case_id,
                    civicrm_contact_id
                FROM i2b2_app03_bioresource_Data.dbo.LOAD_COMBINED_VALID_RECRUITED
                WHERE legacy_bioresource_id IN (
                    SELECT legacy_bioresource_id
                    FROM i2b2_app03_bioresource_Data.dbo.LOAD_COMBINED_VALID_RECRUITED
                    WHERE LEN(RTRIM(LTRIM(legacy_bioresource_id))) > 1
                    GROUP BY legacy_bioresource_id
                    HAVING COUNT(*) > 1
                )
                ORDER BY legacy_bioresource_id
                ''')

            if cursor.rowcount == 0:
                return

            markdown = f'**{REPORT_NAME}**\r\n\r\n'
            markdown += ("_The following recruited participants have "
                         "duplicated legacy ids"
                         "_:\r\n\r\n")

            for row in cursor:
                markdown += '- {}\r\n\r\n'.format(get_case_link(
                    row['legacy_bioresource_id'],
                    row["civicrm_case_id"],
                    row["civicrm_contact_id"]))

            markdown += f"\r\n\r\n{cursor.rowcount + 1} Record(s) Found"

            send_markdown_email(
                REPORT_NAME,
                get_recipient("BIORESOURCE_BLANK_STUDY_ID_RECIPIENT"),
                markdown)
            send_markdown_slack(REPORT_NAME, markdown)


bioresource_legacy_id_duplicates()
schedule.every().monday.at("08:00").do(bioresource_legacy_id_duplicates)


logging.info(f"{REPORT_NAME} Loaded")

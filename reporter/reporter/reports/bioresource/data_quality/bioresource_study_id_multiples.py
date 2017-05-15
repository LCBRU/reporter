#!/usr/bin/env python3

import schedule
import logging
from reporter import (get_report_db, send_markdown_email,
                      send_markdown_slack, get_recipient, get_contact_link)


REPORT_NAME = 'Bioresource Study ID Multiples'


def bioresource_study_id_multiples():

    markdown = ''

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
                SELECT
                      pm1.patient_num
                    , pm1.patient_ide_source
                    , SUBSTRING(ids.id, 3, 2000) AS id
                    , pm_civi.patient_ide AS civicrm_contact_id
                FROM i2b2_app03_bioresource_Data.dbo.patient_mapping pm1
                CROSS APPLY (
                    SELECT
                        [text()] = '; ' + pm2.patient_ide
                    FROM i2b2_app03_bioresource_Data.dbo.patient_mapping pm2
                    WHERE pm1.patient_num = pm2.patient_num
                        AND pm1.patient_ide_source = pm2.patient_ide_source
                    ORDER BY pm2.patient_ide
                    FOR XML PATH('')
                ) ids (id)
                LEFT JOIN i2b2_app03_bioresource_Data.dbo.patient_mapping pm_civi
                    ON pm_civi.patient_num = pm1.patient_num
                    AND pm_civi.patient_ide_source = 'CiviCRM'
                GROUP BY pm1.patient_num
                    , pm1.patient_ide_source
                    , ids.id
                    , pm_civi.patient_ide
                HAVING COUNT(*) > 1
                ''')

            if cursor.rowcount == 0:
                return

            markdown = '**{}**\r\n\r\n'.format(REPORT_NAME)
            markdown += ("_The following participants have "
                         "multiple study IDs"
                         "_:\r\n\r\n")

            for row in cursor:
                markdown += '- {} (IDs \'{}\' of type \'{}\')\r\n'.format(
                    get_contact_link(
                        'Click to View Contact',
                        row["civicrm_contact_id"]),
                    row['id'],
                    row['patient_ide_source']
                )

            markdown += "\r\n\r\n{} Record(s) Found".format(
                cursor.rowcount + 1
            )

            send_markdown_email(
                REPORT_NAME,
                get_recipient("BIORESOURCE_BLANK_STUDY_ID_RECIPIENT"),
                markdown)
            send_markdown_slack(REPORT_NAME, markdown)


# bioresource_study_id_multiples()
schedule.every().monday.at("08:00").do(bioresource_study_id_multiples)


logging.info("{} Loaded".format(REPORT_NAME))

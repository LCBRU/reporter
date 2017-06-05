#!/usr/bin/env python3

from reporter.reports import Report
from reporter import get_contact_link, RECIPIENT_BIORESOURCE_ADMIN


class BioresourceStudyIdMultiplesReport(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "multiple study IDs"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''
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
            HAVING COUNT(*) > 1;
            '''
        )

    def get_report_line(self, row):
        return '- {} (IDs \'{}\' of type \'{}\')\r\n'.format(
            get_contact_link(
                'Click to View Contact',
                row["civicrm_contact_id"]),
            row['id'],
            row['patient_ide_source']
        )

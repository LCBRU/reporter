#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.reports.civicrm import get_contact_link
from reporter.emailing import RECIPIENT_IT_DWH


class PatientMappingDuplicatesReport(SqlReport):
    def __init__(self, database, schedule=None):
        super().__init__(
            introduction='''
                Duplicates found in {} patient_mapping:'''.format(database),
            recipients=[RECIPIENT_IT_DWH],
            schedule=schedule,
            sql='''
                SELECT PATIENT_IDE, PATIENT_IDE_SOURCE, COUNT(*) AS ct
                FROM {}.dbo.Patient_Mapping pm
                GROUP BY PATIENT_IDE, PATIENT_IDE_SOURCE
                HAVING COUNT(*) > 1;
                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {} (ID type = \'{}\')\r\n'.format(
            row['PATIENT_IDE'],
            row['PATIENT_IDE_SOURCE']
        )


class PatientMappingMultiplesIdsReport(SqlReport):
    def __init__(self, database, schedule=None):
        super().__init__(
            introduction=("Paticipants with multiple study "
                          "IDs in {} patient_mapping".format(database)),
            recipients=[RECIPIENT_IT_DWH],
            schedule=schedule,
            sql='''
            SELECT
                  pm1.patient_num
                , pm1.patient_ide_source
                , SUBSTRING(ids.id, 3, 2000) AS id
                , pm_civi.patient_ide AS civicrm_contact_id
            FROM {0}.dbo.patient_mapping pm1
            CROSS APPLY (
                SELECT
                    [text()] = '; ' + pm2.patient_ide
                FROM {0}.dbo.patient_mapping pm2
                WHERE pm1.patient_num = pm2.patient_num
                    AND pm1.patient_ide_source = pm2.patient_ide_source
                ORDER BY pm2.patient_ide
                FOR XML PATH('')
            ) ids (id)
            LEFT JOIN {0}.dbo.patient_mapping pm_civi
                ON pm_civi.patient_num = pm1.patient_num
                AND pm_civi.patient_ide_source = 'CiviCRM'
            GROUP BY pm1.patient_num
                , pm1.patient_ide_source
                , ids.id
                , pm_civi.patient_ide
            HAVING COUNT(*) > 1;
            '''.format(database)
        )

    def get_report_line(self, row):
        return '- {} (IDs \'{}\' of type \'{}\')\r\n'.format(
            get_contact_link(
                'Click to View Contact',
                row["civicrm_contact_id"]),
            row['id'],
            row['patient_ide_source']
        )

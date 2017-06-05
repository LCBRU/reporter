#!/usr/bin/env python3

from reporter.reports import Report
from reporter import RECIPIENT_BIORESOURCE_ADMIN


class BioresourceStudyIdDuplicatesReport(Report):
    def __init__(self):
        super().__init__(
            introduction="The following study IDs are duplicated",
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''
                SELECT PATIENT_IDE, PATIENT_IDE_SOURCE, COUNT(*) AS ct
                FROM i2b2_app03_bioresource_Data.dbo.Patient_Mapping pm
                GROUP BY PATIENT_IDE, PATIENT_IDE_SOURCE
                HAVING COUNT(*) > 1;
                '''
        )

    def get_report_line(self, row):
        return '- {} (ID type = \'{}\')\r\n'.format(
            row['PATIENT_IDE'],
            row['PATIENT_IDE_SOURCE']
        )

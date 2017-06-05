#!/usr/bin/env python3

from reporter.reports import Report
from reporter import RECIPIENT_IT_DWH


class GenvascPatientSummaryDuplicatesReport(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants are duplicated "
                          "in the patient_summary view"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''
                SELECT patient_num, COUNT(*) AS ct
                FROM    i2b2_app03_genvasc_Data.dbo.PatientSummary
                GROUP BY patient_num
                HAVING COUNT(*) > 1;
                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(row['patient_num'])

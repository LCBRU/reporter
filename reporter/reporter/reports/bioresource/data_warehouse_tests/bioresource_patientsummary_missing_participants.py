#!/usr/bin/env python3

from reporter.reports import Report
from reporter import RECIPIENT_IT_DWH


class BioresourcePatientSummaryMissingParticiapnts(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants are "
                          "missing from the patient summary"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''
                SELECT pd.Patient_Num
                FROM i2b2_app03_bioresource_Data.dbo.Patient_Dimension pd
                WHERE pd.Patient_Num NOT IN (
                    SELECT ps.Patient_Num
                    FROM i2b2_app03_bioresource_Data.dbo.PatientSummary ps)
                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(row['patient_num'])

#!/usr/bin/env python3

from reporter.reports import Report
from reporter import get_case_link, RECIPIENT_IT_DWH


class BioresourcePatientSummaryMissingRecruited(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have an error "
                          "so they have not reached i2b2"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

SELECT  civicrm_case_id, civicrm_contact_id
FROM [i2b2_app03_bioresource_Data].[dbo].[LOAD_Civicrm_Bioresource] a
WHERE is_recruited = 1
    AND NOT EXISTS (
        SELECT 1
        FROM [i2b2_app03_bioresource_Data].[dbo].PatientSummary
        WHERE StudyNumber = a.bioresource_id
    )

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                'Click to View',
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))

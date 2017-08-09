#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import get_case_link, RECIPIENT_IT_DWH


class BriccsPatientSummaryMissingRecruited(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have an error "
                          "so they have not reached i2b2"),
            recipients=[RECIPIENT_IT_DWH],
            schedule=Schedule.never,
            sql='''

SELECT  civicrm_case_id, civicrm_contact_id
FROM [i2b2_app03_b1_Data].[dbo].[LOAD_Civicrm] a
WHERE is_recruited = 1
    AND NOT EXISTS (
        SELECT 1
        FROM [i2b2_app03_b1_Data].[dbo].PatientSummary
        WHERE StudyNumber = a.StudyNumber
    )

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                'Click to View',
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))
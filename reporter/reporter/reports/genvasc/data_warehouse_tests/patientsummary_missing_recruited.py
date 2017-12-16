#!/usr/bin/env python3

from reporter.reports import Report
from reporter.reports.emailing import RECIPIENT_IT_DWH
from reporter.reports.civicrm import get_case_link


class GenvascPatientSummaryMissingRecruited(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have an error "
                          "so they have not reached i2b2"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

SELECT
    a.CaseId,
    a.CiviCrmId
FROM i2b2_app03_genvasc_Data.[dbo].LOAD_ValidEnrollments a
WHERE NOT EXISTS (
        SELECT 1
        FROM i2b2_app03_genvasc_Data.[dbo].PatientSummary
        WHERE StudyNumber = a.StudyNumber
    )

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                'Click to View',
                row["CaseId"],
                row["CiviCrmId"]))

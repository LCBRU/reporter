#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import get_case_link, RECIPIENT_BRICCS_DQ


class BriccsCivcrmBlankStudyId(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have a blank "
                          "study ID in the CiviCRM Study Enrolment"),
            recipients=[RECIPIENT_BRICCS_DQ],
            schedule=Schedule.daily,
            sql='''

SELECT civicrm_case_id, civicrm_contact_id
FROM i2b2_app03_b1_Data.dbo.LOAD_Civicrm
WHERE blank_study_id = 1
    AND (
            is_recruited = 1
            OR is_withdrawn = 1
            OR is_duplicate = 1
        )

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                'Click to View',
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))

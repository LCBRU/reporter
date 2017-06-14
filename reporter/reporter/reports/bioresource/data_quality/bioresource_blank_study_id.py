#!/usr/bin/env python3

from reporter.reports import Report
from reporter import get_case_link, RECIPIENT_BIORESOURCE_ADMIN


class BioresourceCivcrmBlankStudyId(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have a blank "
                          "study ID in the CiviCRM Study Enrolment"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''

SELECT civicrm_case_id, civicrm_contact_id
FROM i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Bioresource b
WHERE blank_study_id = 1
    AND (
            b.is_recruited = 1
            OR b.is_excluded = 1
            OR b.is_withdrawn = 1
            OR b.is_duplicate = 1
        )

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                'Click to View',
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))

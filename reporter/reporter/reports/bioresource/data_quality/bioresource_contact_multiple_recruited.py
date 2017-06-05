#!/usr/bin/env python3

from reporter.reports import Report
from reporter import get_contact_link, RECIPIENT_BIORESOURCE_ADMIN


class BioresourceContactMultipleRecruitments(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have multiple "
                          "recruited enrolments"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''
            SELECT civicrm_contact_id
            FROM i2b2_app03_bioresource_Data.dbo.LOAD_COMBINED_VALID_RECRUITED
            GROUP BY civicrm_contact_id
            HAVING COUNT(*) > 1
                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_contact_link('Click to View', row["civicrm_contact_id"]))

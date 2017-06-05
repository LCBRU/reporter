#!/usr/bin/env python3

from reporter.reports import Report
from reporter import get_case_link, RECIPIENT_BIORESOURCE_ADMIN


class BioresourceIdDuplicates(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following recruited participants have "
                          "duplicated bioresource ids"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''
        SELECT
            bioresource_id,
            legacy_bioresource_id,
            civicrm_case_id,
            civicrm_contact_id
        FROM i2b2_app03_bioresource_Data.dbo.LOAD_COMBINED_VALID_RECRUITED
        WHERE bioresource_id IN (
            SELECT bioresource_id
            FROM i2b2_app03_bioresource_Data.dbo.LOAD_COMBINED_VALID_RECRUITED
            GROUP BY bioresource_id
            HAVING COUNT(*) > 1
        )
        ORDER BY bioresource_id
                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                row['bioresource_id'],
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))

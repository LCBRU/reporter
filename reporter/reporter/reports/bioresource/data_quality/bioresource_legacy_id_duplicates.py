#!/usr/bin/env python3

from reporter.reports import Report
from reporter import get_case_link, RECIPIENT_BIORESOURCE_ADMIN


class BioresourceLegacyIdDuplicates(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following recruited participants have "
                          "duplicated legacy ids"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''
        SELECT
            bioresource_id,
            legacy_bioresource_id,
            civicrm_case_id,
            civicrm_contact_id
        FROM i2b2_app03_bioresource_Data.dbo.LOAD_COMBINED_VALID_RECRUITED
        WHERE legacy_bioresource_id IN (
            SELECT legacy_bioresource_id
            FROM i2b2_app03_bioresource_Data.dbo.LOAD_COMBINED_VALID_RECRUITED
            WHERE LEN(RTRIM(LTRIM(legacy_bioresource_id))) > 1
            GROUP BY legacy_bioresource_id
            HAVING COUNT(*) > 1
        )
        ORDER BY legacy_bioresource_id
                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                row['legacy_bioresource_id'],
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))

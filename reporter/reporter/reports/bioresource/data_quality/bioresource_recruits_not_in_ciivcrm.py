#!/usr/bin/env python3

from reporter.reports import Report
from reporter import get_contact_id_search_link, RECIPIENT_BIORESOURCE_ADMIN


class BioresourceNotInCivicrm(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "a record in REDCap, but do not have "
                          "a record in CiviCRM"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''

SELECT  CONVERT(VARCHAR(100), a.bioresource_or_legacy_id) as bioresource_id
FROM i2b2_app03_bioresource_Data.dbo.Load_Fully_Consented a
WHERE NOT EXISTS (
    SELECT 1
    FROM i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Bioresource b
    WHERE (
            a.bioresource_or_legacy_id = b.bioresource_id
            OR a.bioresource_or_legacy_id = b.legacy_bioresource_id
        ) AND (
            b.is_recruited = 1 OR
            b.is_excluded = 1 OR
            b.is_withdrawn = 1 OR
            b.is_duplicate = 1)
)

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_id_search_link(
                row['bioresource_id'], row['bioresource_id'])
        )

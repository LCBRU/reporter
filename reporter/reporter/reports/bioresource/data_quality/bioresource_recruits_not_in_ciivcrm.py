#!/usr/bin/env python3

from reporter.reports import SqlReport
from reporter.reports.emailing import RECIPIENT_IT_DWH


class BioresourceNotInCivicrm(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "a record in REDCap, but do not have "
                          "a record in CiviCRM"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

SELECT  CONVERT(VARCHAR(100), a.bioresource_or_legacy_id) as bioresource_id,
    CASE WHEN interval_consent = 1 THEN 'INTERVAL; ' ELSE '' END
      + CASE WHEN redcap_consent = 1 THEN 'REDCap; ' ELSE '' END
      + CASE WHEN joint_briccs_consent = 1 THEN 'Joint BRICCS; ' ELSE '' END
    AS [context]

FROM i2b2_app03_bioresource_Data.dbo.Load_FullyConsented a
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
        return '- {} {}\r\n'.format(row['bioresource_id'], row['context'])

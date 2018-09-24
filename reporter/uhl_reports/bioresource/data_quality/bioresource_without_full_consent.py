#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.emailing import RECIPIENT_BIORESOURCE_ADMIN
from reporter.uhl_reports.civicrm import get_contact_id_search_link


class BioresourceWithoutFullConsent(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants are recruited or "
                          "duplicates in CiviCRM, but a "
                          "record of full consent cannot be found"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''

SELECT
    CONVERT(VARCHAR(100), b.bioresource_id) as bioresource_id
FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Bioresource b
WHERE
        b.blank_study_id = 0
    AND b.is_recruited = 1
    AND NOT EXISTS (
        SELECT 1
        FROM    i2b2_app03_bioresource_Data.dbo.Load_FullyConsented
        WHERE   StudyNumber = b.bioresource_id
            OR StudyNumber = b.legacy_bioresource_id
    )

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_id_search_link(
                row["bioresource_id"],
                row["bioresource_id"],
            )
        )

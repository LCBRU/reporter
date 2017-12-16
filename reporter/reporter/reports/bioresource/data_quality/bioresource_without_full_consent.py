#!/usr/bin/env python3

from reporter.reports import Report
from reporter.reports.emailing import RECIPIENT_BIORESOURCE_ADMIN
from reporter.reports.civicrm import get_contact_id_search_link


class BioresourceWithoutFullConsent(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants are recruited or "
                          "duplicates in CiviCRM, but a "
                          "record of full consent cannot be found"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''

SELECT
    CONVERT(VARCHAR(100), b.bioresource_id) as bioresource_id,
    b.consent_date
FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Bioresource b
WHERE
        b.blank_study_id = 0
    AND b.is_recruited = 1
    AND NOT EXISTS (
        SELECT 1
        FROM    i2b2_app03_bioresource_Data.dbo.Load_Fully_Consented
        WHERE   bioresource_or_legacy_id = b.bioresource_id
            OR bioresource_or_legacy_id = b.legacy_bioresource_id
    )

                '''
        )

    def get_report_line(self, row):
        consent_date = ('{:%d-%b-%Y}'.format(row["consent_date"])
                        if row['consent_date'] else '')
        return '- {} {}\r\n'.format(
            get_contact_id_search_link(
                row["bioresource_id"],
                row["bioresource_id"]),
            consent_date)

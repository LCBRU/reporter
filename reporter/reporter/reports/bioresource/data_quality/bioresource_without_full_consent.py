#!/usr/bin/env python3

from reporter.reports import Report
from reporter import get_contact_id_search_link, RECIPIENT_BIORESOURCE_ADMIN


class BioresourceWithoutFullConsent(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants are recruited, "
                          "duplicates or withdrawn in CiviCRM, but a "
                          "record of full consent cannot be found"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''
                SELECT  bioresource_id,
                        consent_date
                FROM    CIVICRM_ScheduledReports_Bioresource_WithoutFullConsent
                ORDER BY bioresource_id
                '''
        )

    def get_report_line(self, row):
        consent_date = ('{}:%d-%b-%Y}'.format(row["consent_date"])
                        if row['consent_date'] else '')
        return '- {} {}\r\n'.format(
            get_contact_id_search_link(
                row["bioresource_id"],
                row["bioresource_id"]),
            consent_date)

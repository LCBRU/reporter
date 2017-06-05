#!/usr/bin/env python3

from reporter.reports import Report
from reporter import get_contact_id_search_link, RECIPIENT_BIORESOURCE_ADMIN


class BioresourceNotInRedcap(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "a record in CiviCRM, but do not have "
                          "a record in REDCap"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''
                SELECT  bioresource_id,
                        consent_date
                FROM CIVICRM_ScheduledReports_Bioresource_RecruitsNotInRedcap
                ORDER BY consent_date, bioresource_id
                '''
        )

    def get_report_line(self, row):
        return '- {} {}\r\n'.format(
            get_contact_id_search_link(
                row['bioresource_id'], row['bioresource_id']),
            '{:%d-%b-%Y}'.format(row['consent_date'])
            if row['consent_date'] else ''
        )

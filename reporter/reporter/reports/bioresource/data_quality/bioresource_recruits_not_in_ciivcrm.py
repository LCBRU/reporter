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
                SELECT  bioresource_id
                FROM CIVICRM_ScheduledReports_Bioresource_RecruitsNotInCiviCrm
                ORDER BY bioresource_id
                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_id_search_link(
                row['bioresource_id'], row['bioresource_id'])
        )

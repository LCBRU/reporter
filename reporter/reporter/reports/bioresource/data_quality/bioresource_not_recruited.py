#!/usr/bin/env python3

from reporter.reports import Report
from reporter.reports.emailing import RECIPIENT_BIORESOURCE_ADMIN
from reporter.reports.civicrm import get_contact_id_search_link


class BioresourceConsentedNotRecruited(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants appear "
                          "to have full consent, but do not have a status "
                          "of recruited in CiviCRM"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''
                SELECT bioresource_id,
                       consent_date
                FROM CIVICRM_ScheduledReports_Bioresource_NotRecruited
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

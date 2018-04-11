#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.reports.civicrm import get_contact_link
from reporter.emailing import RECIPIENT_IT_DQ


class CivicrmInvalidPostCode(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following contacts have an address "
                          "with an invalid post code"),
            recipients=[RECIPIENT_IT_DQ],
            sql='''
SELECT
    con.id AS contact_id,
    a.postal_code
FROM STG_CiviCRM.dbo.civicrm_address a
JOIN STG_CiviCRM.dbo.civicrm_contact con
    ON con.id = a.contact_id
    AND con.is_deleted = 0
WHERE i2b2ClinDataIntegration.dbo.isInvalidPostcode(postal_code) = 1
    AND a.country_id = 1226 -- UK

                ''',
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_link(row['postal_code'], row['contact_id'])
        )

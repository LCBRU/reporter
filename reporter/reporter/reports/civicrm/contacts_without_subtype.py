#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import get_contact_link, RECIPIENT_IT_DQ


class CivicrmContactsWithoutSubtypes(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following contacts do not have "
                          "a subtype"),
            recipients=[RECIPIENT_IT_DQ],
            sql='''
SELECT
    id AS contact_id,
    contact_type
FROM STG_CiviCRM.dbo.civicrm_contact
WHERE LTRIM(RTRIM(ISNULL(contact_sub_type, ''))) = ''
    AND is_deleted = 0
;
                ''',
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_link(row['contact_type'], row['contact_id'])
        )

#!/usr/bin/env python3

from reporter.reports import SqlReport, Schedule
from reporter.reports.civicrm import get_contact_link
from reporter.reports.emailing import RECIPIENT_IT_DQ


class CivicrmSubjectDuplicateNameAndDob(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following subjects have "
                          "a duplicate Name and DOB in CiviCRM"),
            recipients=[RECIPIENT_IT_DQ],
            sql='''

SELECT
    con1.id [subject_a_id],
    con1.display_name,
    con1.birth_date,
    con2.id [subject_b_id],
    con2.display_name,
    con2.birth_date
FROM    STG_CiviCRM.dbo.civicrm_contact con1
JOIN    STG_CiviCRM.dbo.civicrm_contact con2
    ON con2.first_name = con1.first_name
    AND con2.last_name = con1.last_name
    AND (
            (con2.birth_date IS NULL AND con1.birth_date IS NULL)
            OR con2.birth_date = con1.birth_date
        )
    AND con2.id <> con1.id
    AND con2.contact_sub_type = con1.contact_sub_type
WHERE con1.contact_sub_type = 'Subject'

                ''',
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {} <-> {}\r\n'.format(
            get_contact_link('Subject A', row['subject_a_id']),
            get_contact_link('Subject B', row['subject_b_id'])
        )

#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter.reports.civicrm import get_contact_link
from reporter.reports.emailing import RECIPIENT_IT_DQ


class CivicrmNonSubjectEnrolledToStudy(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following contacts have an enrollment "
                          "in a study in CiviCRM, but do not have "
                          "a type of Subject"),
            recipients=[RECIPIENT_IT_DQ],
            sql='''

SELECT con.id AS contact_id
FROM    STG_CiviCRM.dbo.civicrm_contact con
WHERE   con.contact_sub_type NOT LIKE '%Subject%'
    AND con.is_deleted = 0
    AND EXISTS (
        SELECT 1
        FROM    STG_CiviCRM.dbo.civicrm_case_contact cas_con
        JOIN    STG_CiviCRM.dbo.civicrm_case cas
            ON cas.id = cas_con.case_id
            AND cas.is_deleted = 0
            AND cas.case_type_id NOT IN (13) -- GENVASC Site Management
        WHERE cas_con.contact_id = con.id

    )
;
                ''',
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_link('Click here to see contact', row['contact_id'])
        )

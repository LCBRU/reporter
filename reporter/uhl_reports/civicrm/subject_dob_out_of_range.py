#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.uhl_reports.civicrm import get_contact_link
from reporter.emailing import RECIPIENT_IT_DQ


class CivicrmSubjectDobOutOfRange(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following subjects have "
                          "a DOB that is out of range in CiviCRM"),
            recipients=[RECIPIENT_IT_DQ],
            sql='''

SELECT DISTINCT
    con.id AS contact_id
FROM STG_CiviCRM.dbo.civicrm_contact con
LEFT JOIN STG_CiviCRM.dbo.civicrm_case_contact cc
    ON cc.contact_id = con.id
LEFT JOIN STG_CiviCRM.dbo.civicrm_case cas
    ON cas.id = cc.case_id
WHERE con.is_deleted = 0
    AND con.birth_date IS NOT NULL
    AND (   YEAR(con.birth_date) < 1914
            OR YEAR(con.birth_date) > 2009
            OR (    YEAR(con.birth_date) > 2001
                    AND  cas.case_type_id <> 10 -- Not BRAVE
                )
    )

                ''',
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_link('Subject', row['contact_id'])
        )

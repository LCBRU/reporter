#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import (
    RECIPIENT_TMAO_ADMIN,
    get_case_link
)


class TmaoCiviCrmMissingStudyNumber(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following TMAO enrolments do not have "
                          "study numbers in CiviCRM"),
            recipients=[RECIPIENT_TMAO_ADMIN],
            sql='''

SELECT
    cas.id AS case_id,
    con.id AS contact_id
FROM    STG_CiviCRM.dbo.civicrm_case cas
JOIN    STG_CiviCRM.dbo.civicrm_case_contact cas_con
    ON cas_con.case_id = cas.id
JOIN    STG_CiviCRM.dbo.civicrm_contact con
    ON con.id = cas_con.contact_id
    AND con.is_deleted = 0
JOIN    STG_CiviCRM.dbo.civicrm_value_tmao_18 tmao
    ON tmao.entity_id = cas.id
WHERE cas.is_deleted = 0
    AND cas.case_type_id = 12 -- TMAO
    AND cas.status_id IN (
        5, --recruited
        8  -- withdrawn
    )
    AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(tmao.tmao_id_79) = 1;

                ''',
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_case_link(
                'Click Here',
                row['case_id'],
                row['contact_id']))

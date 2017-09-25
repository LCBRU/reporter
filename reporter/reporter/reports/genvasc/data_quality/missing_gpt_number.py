#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import get_case_link, RECIPIENT_GENVASC_ADMIN


class GenvascMissingGptNumber(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following recruitments "
                          "do not have a GPT number"),
            schedule=Schedule.daily,
            recipients=[RECIPIENT_GENVASC_ADMIN],
            sql='''

SELECT
    cas.id [civicrm_case_id],
    cas_con.contact_id [civicrm_contact_id]
FROM    STG_CiviCRM.dbo.civicrm_case cas
JOIN    STG_CiviCRM.dbo.civicrm_case_contact cas_con
    ON cas_con.case_id = cas.id
JOIN    STG_CiviCRM.dbo.civicrm_contact con
    ON con.id = cas_con.contact_id
    AND con.is_deleted = 0
LEFT JOIN    STG_CiviCRM.dbo.civicrm_value_genvasc_recruitment_data_5 gen
    ON gen.entity_id = cas.id
WHERE cas.case_type_id = 3 -- GENVASC
    AND cas.is_deleted = 0
    AND cas.status_id IN (
        5, -- Recruited
        6, -- Available for cohort
        8) -- Withdrawn
    AND LEN(RTRIM(LTRIM(COALESCE(gen.genvasc_id_10, '')))) = 0

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                'Click to View',
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))

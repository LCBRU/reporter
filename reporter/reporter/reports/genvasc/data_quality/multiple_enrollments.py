#!/usr/bin/env python3

from itertools import groupby
from reporter.reports import Report, Schedule
from reporter import get_contact_link, RECIPIENT_GENVASC_ADMIN


class GenvascMultipleEnrollments(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following recruitments "
                          "have multiple enrollments:"),
            schedule=Schedule.daily,
            recipients=[RECIPIENT_GENVASC_ADMIN],
            sql='''

WITH x AS (
    SELECT
        cas_con.contact_id [civicrm_contact_id],
        gen.genvasc_id_10 [StudyNumber]
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
)
SELECT *
FROM    x
WHERE civicrm_contact_id IN (
    SELECT civicrm_contact_id
    FROM x
    GROUP BY civicrm_contact_id
    HAVING COUNT(*) > 1
)
ORDER BY civicrm_contact_id

                '''
        )

    def get_report_lines(self, cursor):
        markdown = ''
        cnt = 0

        for cid, g in groupby(cursor, lambda r: r['civicrm_contact_id']):
            markdown += "{}\r\n\r\n".format(get_contact_link(
                ', '.join([r['StudyNumber'] for r in g]),
                cid
            ))
            cnt += 1

        return markdown, cnt

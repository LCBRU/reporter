#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter.reports.emailing import (
    RECIPIENT_FAST_MANAGER,
    RECIPIENT_FAST_ADMIN,
)


class FastWithdrawnWithDataReport(Report):
    def __init__(self):
        super().__init__(
            introduction=("Withdrawn participants with data "
                          "in REDCap for FAST study"),
            recipients=[RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN],
            schedule=Schedule.weekly,
            sql='''

SELECT record [StudyNumber]
FROM    [STG_redcap].dbo.redcap_data rd_wd
WHERE   rd_wd.project_id = 43 -- FAST
    AND rd_wd.field_name = 'wthdrwl_date'
    AND rd_wd.value IS NOT NULL
    AND EXISTS (
        SELECT 1
        FROM    [STG_redcap].dbo.redcap_data rd
        JOIN    [STG_redcap].dbo.redcap_metadata meta
            ON meta.project_id = rd.project_id
            AND meta.field_name = rd.field_name
            AND meta.form_name NOT IN (
                'withdrawal',
                'consent',
                'screening_event'
            )
        WHERE rd.project_id = rd_wd.project_id
            AND rd.record = rd_wd.record
    )

                '''
        )

    def get_report_lines(self, cursor):
        markdown = ''

        for p in cursor:
            markdown += "- {}\r\n".format(p['StudyNumber'])

        markdown += "\r\n\r\n".format()

        return markdown, cursor.rowcount + 1

#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter.reports.emailing import (
    RECIPIENT_MARI_MANAGER,
    RECIPIENT_MARI_ADMIN
)


class MariWithdrawnWithDataReport(Report):
    def __init__(self):
        super().__init__(
            introduction=("Withdrawn participants with data "
                          "in REDCap for MARI study"),
            recipients=[
                RECIPIENT_MARI_MANAGER,
                RECIPIENT_MARI_ADMIN],
            schedule=Schedule.weekly,
            sql='''

SELECT record [StudyNumber]
FROM    [STG_redcap].dbo.redcap_data rd_wd
WHERE   rd_wd.project_id = 52 -- MARI
    AND rd_wd.field_name = 'reason_for_participant_rem'
    AND rd_wd.value = '6' -- Withdrawal of consent
    AND EXISTS (
        SELECT 1
        FROM    [STG_redcap].dbo.redcap_data rd
        JOIN    [STG_redcap].dbo.redcap_metadata meta
            ON meta.project_id = rd.project_id
            AND meta.field_name = rd.field_name
            AND meta.form_name NOT IN (
                'study_status_and_validation',
                'consent'
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

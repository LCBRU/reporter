#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.emailing import (
    RECIPIENT_MARI_MANAGER,
    RECIPIENT_MARI_ADMIN
)


class MariWithdrawnWithDataReport(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("Withdrawn participants with data "
                          "in REDCap for MARI study"),
            recipients=[
                RECIPIENT_MARI_MANAGER,
                RECIPIENT_MARI_ADMIN],
            schedule=Schedule.never,
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
        count = 0

        for p in cursor:
            count += 1
            markdown += "- {}\r\n".format(p['StudyNumber'])

        markdown += "\r\n\r\n".format()

        return markdown, count

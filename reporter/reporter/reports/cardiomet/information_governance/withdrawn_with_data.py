#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.emailing import (
    RECIPIENT_CARDIOMET_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_CARDIOMET_ADMIN as RECIPIENT_ADMIN,
)


class CardiometWithdrawnWithDataReport(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("Withdrawn participants with data "
                          "in REDCap study"),
            recipients=[
                RECIPIENT_MANAGER,
                RECIPIENT_ADMIN],
            schedule=Schedule.weekly,
            sql='''

SELECT record [StudyNumber]
FROM    [STG_redcap].dbo.redcap_data rd_wd
WHERE   rd_wd.project_id = 50 -- Indapamide
    AND rd_wd.field_name = 'non_complete_rsn'
    AND rd_wd.value = '5' -- Withdrawal of consent
    AND EXISTS (
        SELECT 1
        FROM    [STG_redcap].dbo.redcap_data rd
        JOIN    [STG_redcap].dbo.redcap_metadata meta
            ON meta.project_id = rd.project_id
            AND meta.field_name = rd.field_name
            AND meta.form_name NOT IN (
                'study_status',
                'study_details',
                'participant_details'
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

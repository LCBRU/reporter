#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import RECIPIENT_INDAPAMIDE_MANAGER, RECIPIENT_INDAPAMIDE_ADMIN


class IndapamideWithdrawnWithDataReport(Report):
    def __init__(self):
        super().__init__(
            introduction=("Withdrawn participants with data "
                          "in REDCap for Indapamide study"),
            recipients=[
                RECIPIENT_INDAPAMIDE_MANAGER,
                RECIPIENT_INDAPAMIDE_ADMIN],
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

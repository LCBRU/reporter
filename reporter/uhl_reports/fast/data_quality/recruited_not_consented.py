#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.emailing import (
    RECIPIENT_FAST_MANAGER,
    RECIPIENT_FAST_ADMIN,
)
from reporter.connections import get_redcap_link


class FastRecruitedNotConsentedReport(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following FAST participants are "
                          "recruited, but do not have full consent:"),
            recipients=[RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN],
            schedule=Schedule.weekly,
            sql='''
WITH recruited AS (
    SELECT
        fast_id.record,
        fast_id.value AS fast_id
    FROM    STG_redcap.dbo.redcap_data recruited
    JOIN    STG_redcap.dbo.redcap_data fast_id
        ON fast_id.record = recruited.record
        AND fast_id.field_name = 'fst_label'
    WHERE recruited.project_id = 48
        AND recruited.field_name = 'patient_recruited'
        AND recruited.value = 1
)
SELECT  fast_id
FROM    recruited
WHERE NOT EXISTS (
    SELECT 1
    FROM    i2b2_app03_fast_Data.dbo.LOAD_FullyConsented fc
    WHERE fc.StudyNumber = recruited.fast_id
)

                '''
        )

    def get_report_lines(self, cursor):
        markdown = ''

        for p in cursor:
            markdown += "- **{}**\r\n".format(get_redcap_link(
                p['fast_id'], 43, p['fast_id']))

        markdown += "\r\n\r\n".format()

        return markdown, cursor.rowcount + 1

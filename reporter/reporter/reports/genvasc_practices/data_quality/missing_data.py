#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import (
    get_redcap_external_link,
    RECIPIENT_GENVASC_MANAGER, RECIPIENT_GENVASC_ADMIN
)


class GenvascPracticesMissingDataReport(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following GENVASC practices have "
                          "missing data:"),
            recipients=[RECIPIENT_GENVASC_MANAGER, RECIPIENT_GENVASC_ADMIN],
            schedule=Schedule.weekly,
            sql='''

WITH practices (project_id, record) AS (
    SELECT  DISTINCT project_id, record
    FROM    STG_redcap_briccsext.dbo.redcap_data
    WHERE   project_id IN (29, 53)
)
SELECT  p.project_id, p.record, 'Practice Name has not been set' AS message
FROM practices p
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap_briccsext.dbo.redcap_data rd
    WHERE rd.project_id = p.project_id
        AND rd.record = p.record
        AND rd.field_name = 'practice_name'
        AND LEN(RTRIM(LTRIM(COALESCE(rd.value, '')))) > 0
)
UNION
SELECT  p.project_id, p.record, 'Practice Code has not been set'
FROM practices p
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap_briccsext.dbo.redcap_data rd
    WHERE rd.project_id = p.project_id
        AND rd.record = p.record
        AND rd.field_name = 'practice_code'
        AND LEN(RTRIM(LTRIM(COALESCE(rd.value, '')))) > 0
)
;

                '''
        )

    def get_report_lines(self, cursor):
        markdown = ''

        for p in cursor:
            markdown += "- **{}**\r\n".format(get_redcap_external_link(
                '{}: {}'.format(p['record'], p['message']),
                p['project_id'],
                p['record'])
            )

        markdown += "\r\n\r\n".format()

        return markdown, cursor.rowcount + 1

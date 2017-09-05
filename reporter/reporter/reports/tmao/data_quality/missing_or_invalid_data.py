#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import RECIPIENT_TMAO_MANAGER, RECIPIENT_TMAO_ADMIN


class TmaoMissingOrInvalidDataReport(Report):
    def __init__(self):
        super().__init__(
            introduction=("Missing or invalid required data "
                          "in REDCap for TMAO study"),
            recipients=[RECIPIENT_TMAO_MANAGER, RECIPIENT_TMAO_ADMIN],
            schedule=Schedule.weekly,
            sql='''

WITH recruited AS (
    SELECT
        tmao_id.record,
        tmao_id.value AS tmao_id,
        tmao_id.project_id
    FROM    STG_redcap.dbo.redcap_data tmao_id
    WHERE tmao_id.project_id = 25
        AND tmao_id.field_name = 'record_id'
)
SELECT
    r.tmao_id,
    'Missing Gender' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name = 'tmao_gender'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.tmao_id,
    'Missing Ethnicity' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name = 'how_would_you_best_describ'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.tmao_id,
    'Missing Date of Birth' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name = 'tmao_dob'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.tmao_id,
    'Invalid Date of Birth: ' + e.value [error_message]
FROM recruited r
JOIN STG_redcap.dbo.redcap_data e
    ON e.project_id = r.project_id
    AND e.record = r.record
    AND e.field_name = 'tmao_dob'
    AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
    AND ISDATE(e.value) = 0
UNION
SELECT
    r.tmao_id,
    'Invalid Date of Birth: ' + e.value [error_message]
FROM recruited r
JOIN STG_redcap.dbo.redcap_data e
    ON e.project_id = r.project_id
    AND e.record = r.record
    AND e.field_name = 'tmao_dob'
    AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
    AND ISDATE(e.value) = 1
    AND YEAR(e.value) < 1900
UNION
SELECT
    r.tmao_id,
    'Invalid Study Number' [error_message]
FROM recruited r
WHERE tmao_id NOT LIKE 'TMAO[0-9][0-9][0-9][0-9]'
ORDER BY tmao_id

                '''
        )

    def get_report_lines(self, cursor):
        markdown = ''

        for p in cursor:
            markdown += "- **{}** {}\r\n".format(
                p['tmao_id'], p['error_message'])

        markdown += "\r\n\r\n".format()

        return markdown, cursor.rowcount + 1


r = TmaoMissingOrInvalidDataReport()
r.run()

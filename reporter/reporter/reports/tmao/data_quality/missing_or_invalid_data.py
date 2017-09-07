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
        id.record,
        id.value AS study_id,
        id.project_id
    FROM    STG_redcap.dbo.redcap_data id
    WHERE id.project_id = 25
        AND id.field_name = 'record_id'
)

SELECT
    r.study_id,
    'Missing: ' + md.element_label AS [error_message]
FROM recruited r
JOIN STG_redcap.dbo.redcap_metadata md
    ON md.project_id = r.project_id
WHERE md.field_name IN (
    'tmao_gender',
    'how_would_you_best_describ',
    'tmao_dob',
    'are_you_a_vegan',
    'do_you_take_nutritional_su',
    'how_many_per_times_week_do'
) AND NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name = md.field_name
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)

UNION

SELECT
    r.study_id,
    'Missing: ' + md.element_label
FROM recruited r
JOIN STG_redcap.dbo.redcap_metadata md
    ON md.project_id = r.project_id
WHERE md.field_name IN (
    'how_many_times_per_week_do',
    'how_many_times_pork',
    'how_many_times_lamb'
) AND NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name = md.field_name
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
) AND EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name = 'do_you_eat_red_meat'
        AND e.value = 1
)

UNION

SELECT
    r.study_id,
    'Missing: ' + md.element_label
FROM recruited r
JOIN STG_redcap.dbo.redcap_metadata md
    ON md.project_id = r.project_id
WHERE md.field_name IN (
    'do_you_eat_eggs',
    'do_you_eat_red_meat'
) AND NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name = md.field_name
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
) AND EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name = 'are_you_a_vegan'
        AND e.value = 0
)

UNION

SELECT
    r.study_id,
    'Missing: ' + md.element_label
FROM recruited r
JOIN STG_redcap.dbo.redcap_metadata md
    ON md.project_id = r.project_id
WHERE md.field_name IN (
    'how_many_eggs_in_a_week'
) AND NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name = md.field_name
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
) AND EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name = 'do_you_eat_eggs'
        AND e.value = 1
)

UNION

SELECT
    r.study_id,
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
    r.study_id,
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
    r.study_id,
    'Invalid Study Number' [error_message]
FROM recruited r
WHERE study_id NOT LIKE 'TMAO[0-9][0-9][0-9][0-9]'

ORDER BY study_id

                '''
        )

    def get_report_lines(self, cursor):
        markdown = ''

        for p in cursor:
            markdown += "- **{}** {}\r\n".format(
                p['study_id'], p['error_message'])

        markdown += "\r\n\r\n".format()

        return markdown, cursor.rowcount + 1

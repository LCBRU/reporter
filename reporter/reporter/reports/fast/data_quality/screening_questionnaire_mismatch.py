#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN


class FastScreeningQuestionnaireMismatchReport(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following FAST participants have "
                          "a mismatch between the screening and "
                          "questionnaire data in REDCap:"),
            recipients=[RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN],
            schedule=Schedule.weekly,
            sql='''
WITH screening AS (
    SELECT
        fast_id.record,
        fast_id.value AS fast_id,
        fast_id.project_id
    FROM    STG_redcap.dbo.redcap_data recruited
    JOIN    STG_redcap.dbo.redcap_data fast_id
        ON fast_id.record = recruited.record
        AND fast_id.field_name = 'fst_label'
    WHERE recruited.project_id = 48
        AND recruited.field_name = 'patient_reruited'
        AND recruited.value = 1
), questionnaire AS (
    SELECT
        record,
        value AS fast_id,
        project_id
    FROM    STG_redcap.dbo.redcap_data
    WHERE project_id = 43
        AND field_name = 'study_id'
)
SELECT
    s.fast_id,
    'Practice does not match' AS [error_message]
FROM    screening s
JOIN    questionnaire q
    ON q.fast_id = s.fast_id
JOIN    STG_redcap.dbo.redcap_data sd
    ON sd.project_id = s.project_id
    AND sd.record = s.record
    AND sd.field_name = 'gp_practice'
JOIN    STG_redcap.dbo.redcap_data qd
    ON qd.record = q.record
    AND qd.project_id = q.project_id
    AND qd.field_name = 'practice_location'
WHERE qd.value <> sd.value
UNION
SELECT
    s.fast_id,
    'Invitation Group does not match' AS [error_message]
FROM    screening s
JOIN    questionnaire q
    ON q.fast_id = s.fast_id
JOIN    STG_redcap.dbo.redcap_data sd
    ON sd.project_id = s.project_id
    AND sd.record = s.record
    AND sd.field_name = 'invitation_group'
JOIN    STG_redcap.dbo.redcap_data qd
    ON qd.record = q.record
    AND qd.project_id = q.project_id
    AND qd.field_name = 'invitation_grp'
WHERE qd.value <> sd.value
UNION
SELECT
    s.fast_id,
    'NHS Number does not match' AS [error_message]
FROM    screening s
JOIN    questionnaire q
    ON q.fast_id = s.fast_id
JOIN    STG_redcap.dbo.redcap_data sd
    ON sd.project_id = s.project_id
    AND sd.record = s.record
    AND sd.field_name = 'nhs_no'
JOIN    STG_redcap.dbo.redcap_data qd
    ON qd.record = q.record
    AND qd.project_id = q.project_id
    AND qd.field_name = 'nhs_number'
WHERE qd.value <> sd.value

ORDER BY fast_id


                '''
        )

    def get_report_lines(self, cursor):
        markdown = ''

        for p in cursor:
            markdown += "- **{}** {}\r\n".format(
                p['fast_id'], p['error_message'])

        markdown += "\r\n\r\n".format()

        return markdown, cursor.rowcount + 1


r = FastScreeningQuestionnaireMismatchReport()
r.run()

#!/usr/bin/env python3

from itertools import groupby
from reporter.core import SqlReport, Schedule


class RedcapWithdrawnOrExcludedWithDataReport(SqlReport):
    def __init__(self, study_name, recipients):
        super().__init__(
            name="Withdrawn or Excluded with Data Report ({})".format(
                study_name),
            introduction=("Withdrawn or excluded participants with date"
                          "in REDCap for {} study".format(study_name)),
            recipients=recipients,
            schedule=Schedule.weekly,
            sql='''

SELECT
    p.app_title AS [Questionnaire],
    cas.StudyNumber
FROM    [STG_CiviCRM].[dbo].[LCBRU_CaseDetails] cas
JOIN STG_redcap.[dbo].[redcap_project_civicrm_case_type] sxr
    ON sxr.case_type_id = cas.case_type_id
JOIN    STG_redcap.dbo.redcap_projects p
    ON p.project_id = sxr.project_id
WHERE cas.case_type_name = %s
    AND blank_study_number = 0
    AND (
        cas.is_withdrawn = 1
        OR cas.is_excluded = 1
    ) AND EXISTS (
        SELECT 1
        FROM    STG_redcap.dbo.redcap_data rd
        JOIN    STG_redcap.dbo.redcap_metadata meta
            ON meta.project_id = rd.project_id
                AND meta.field_name = rd.field_name
                AND meta.form_name NOT IN (
                    'screening',
                    'consent'
                )
        WHERE   rd.project_id = sxr.project_id
            AND rd.record = cas.StudyNumber
    )
ORDER BY Questionnaire, StudyNumber

                ''',
            parameters=(study_name),
        )

    def get_report_lines(self, cursor):
        markdown = ''

        for questionnaire, participants in groupby(
                cursor,
                lambda x: x['Questionnaire']):

            markdown += "**{}**\r\n\r\n".format(questionnaire)

            for p in participants:
                markdown += "- {}\r\n".format(p['StudyNumber'])

            markdown += "\r\n\r\n".format()

        return markdown, cursor.rowcount + 1

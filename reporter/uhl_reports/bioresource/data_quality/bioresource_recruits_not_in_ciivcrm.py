#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.emailing import RECIPIENT_IT_DWH


class BioresourceNotInCivicrm(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "a record in REDCap, but do not have "
                          "a record in CiviCRM"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

SELECT record
FROM STG_redcap.dbo.all_projects_fully_consented redcap
WHERE project_id = 9
    AND NOT EXISTS (
        SELECT 1
        FROM [STG_CiviCRM].[dbo].[LCBRU_CaseDetails] civi
        JOIN STG_CiviCRM.dbo.civicrm_value_nihr_bioresource_11 bio
            ON bio.entity_id = civi.civicrm_case_id
        WHERE civi.case_type_id = 7
            AND (   civi.StudyNumber = redcap.record
                    OR  bio.nihr_bioresource_legacy_id_78 = redcap.record)
    )


                ''',
            schedule=Schedule.never,
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(row['record'])

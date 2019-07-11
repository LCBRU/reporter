#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.connections import get_redcap_link
from reporter.uhl_reports.civicrm import get_case_link
from reporter.emailing import (
    RECIPIENT_IT_DWH
)


STUDY_NUMBERS_SQL = '''
    WITH c (StudyNumber, civicrm_case_id, civicrm_contact_id) AS (
        SELECT  DISTINCT
            SUBSTRING(StudyNumber, PATINDEX('%[^0]%', StudyNumber + '.'), LEN(StudyNumber)) StudyNumber,
            civicrm_case_id,
            civicrm_contact_id
        FROM    STG_CiviCRM.dbo.LCBRU_CaseDetails
        WHERE   case_type_id IN ({0})
            AND case_status_id IN (
                5, -- Recruited
                8, -- Withdrawn
                9, -- Excluded
                10 -- Completed
            )
            AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(StudyNumber) = 0
    ), r (StudyNumber, project_id) AS (
        SELECT  DISTINCT
            SUBSTRING(record, PATINDEX('%[^0]%', record + '.'), LEN(record)) StudyNumber,
            project_id
        FROM    {2}.dbo.redcap_data
        WHERE project_id IN ({1})
            AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(record) = 0
    )
'''


class CivicrmNotInRedcap(SqlReport):
    def __init__(
            self,
            case_type_ids,
            redcap_project_ids,
            recipients=[RECIPIENT_IT_DWH],
            schedule=None,
            staging_redcap_database='STG_redcap',
    ):
        super().__init__(
            introduction=("The following participants have "
                          "are recruited in CiviCrm, but do not have "
                          "a record in REDCap"),
            recipients=recipients,
            sql=STUDY_NUMBERS_SQL.format(
                    ', '.join(['%s'] * len(case_type_ids)),
                    ', '.join(['%s'] * len(redcap_project_ids)),
                    staging_redcap_database,
                ) + '''
                SELECT
                    StudyNumber,
                    civicrm_case_id,
                    civicrm_contact_id
                FROM c
                WHERE c.StudyNumber NOT IN (
                    SELECT StudyNumber
                    FROM r
                )
                ''',
            parameters=(*case_type_ids, *redcap_project_ids)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_case_link(
                row['StudyNumber'] or 'Click Here',
                row['civicrm_case_id'],
                row['civicrm_contact_id'],
            ))


class RedcapNotInCiviCrm(SqlReport):
    def __init__(
            self,
            case_type_ids,
            redcap_project_ids,
            recipients=[RECIPIENT_IT_DWH],
            schedule=None,
            staging_redcap_database='STG_redcap',
    ):
        super().__init__(
            introduction=("The following participants "
                          "are recruited in REDCap, but do not have "
                          "a record in CiviCRM"),
            recipients=recipients,
            sql=STUDY_NUMBERS_SQL.format(
                    ', '.join(['%s'] * len(case_type_ids)),
                    ', '.join(['%s'] * len(redcap_project_ids)),
                    staging_redcap_database,
                ) + '''
                SELECT
                    StudyNumber,
                    project_id
                FROM r
                WHERE r.StudyNumber NOT IN (
                    SELECT StudyNumber
                    FROM c
                )
                ''',
            parameters=(*case_type_ids, *redcap_project_ids)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_redcap_link(
                row['StudyNumber'] or 'Click Here',
                row['project_id'],
                row['StudyNumber'],
            ))

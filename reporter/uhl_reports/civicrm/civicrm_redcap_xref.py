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
            StudyNumber,
            civicrm_case_id,
            civicrm_contact_id
        FROM    STG_CiviCRM.dbo.LCBRU_CaseDetails
        WHERE   case_type_id = %s
            AND case_status_id IN (
                5, -- Recruited
                8, -- Withdrawn
                9, -- Excluded
                10 -- Completed
            )
            AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(StudyNumber) = 0
    ), r (StudyNumber, project_id) AS (
        SELECT  DISTINCT
            record AS StudyNumber,
            project_id
        FROM    STG_redcap.dbo.redcap_data
        WHERE project_id = %s
            AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(record) = 0
    )
'''


class CivicrmNotInRedcap(SqlReport):
    def __init__(
            self,
            case_type_id,
            redcap_project_id,
            recipients=[RECIPIENT_IT_DWH],
            schedule=None
    ):
        super().__init__(
            introduction=("The following participants have "
                          "are recruited in CiviCrm, but do not have "
                          "a record in REDCap"),
            recipients=recipients,
            sql=STUDY_NUMBERS_SQL + '''
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
            parameters=(case_type_id, redcap_project_id)
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
            case_type_id,
            project_id,
            recipients=[RECIPIENT_IT_DWH],
            schedule=None
    ):
        super().__init__(
            introduction=("The following participants have "
                          "are recruited in CiviCrm, but do not have "
                          "a record in REDCap"),
            recipients=recipients,
            sql=STUDY_NUMBERS_SQL + '''
                SELECT
                    StudyNumber,
                    project_id
                FROM r
                WHERE r.StudyNumber NOT IN (
                    SELECT StudyNumber
                    FROM c
                )
                ''',
            parameters=(case_type_id, project_id)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_redcap_link(
                row['StudyNumber'] or 'Click Here',
                row['project_id'],
                row['StudyNumber'],
            ))

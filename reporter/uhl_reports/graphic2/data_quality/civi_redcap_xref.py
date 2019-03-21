#!/usr/bin/env python3

from reporter.core import Schedule, SqlReport
from reporter.connections import get_redcap_link
from reporter.uhl_reports.civicrm import get_case_link
from reporter.emailing import (
    RECIPIENT_IT_DWH
)

CASE_TYPE_ID = 5
GRAPHIC2_REDCAP_PROJECT_ID = 20


STUDY_NUMBERS_SQL = '''
    WITH c (StudyNumber, civicrm_case_id, civicrm_contact_id) AS (
        SELECT  DISTINCT
            SUBSTRING(StudyNumber, PATINDEX('%[^0]%', StudyNumber + '.'), LEN(StudyNumber)) StudyNumber,
            civicrm_case_id,
            civicrm_contact_id
        FROM    STG_CiviCRM.dbo.LCBRU_CaseDetails
        WHERE   case_type_id = %s
            AND case_status_id IN (
                5 -- Recruited
            )
            AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(StudyNumber) = 0
    ), r (StudyNumber, project_id) AS (
        SELECT  DISTINCT
            SUBSTRING(record, PATINDEX('%[^0]%', record + '.'), LEN(record)) StudyNumber,
            project_id
        FROM    STG_redcap.dbo.redcap_data
        WHERE project_id = %s
            AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(record) = 0
    )
'''


class Graphic2CivicrmNotInRedcap(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "are recruited in CiviCrm, but do not have "
                          "a record in REDCap"),
            recipients=[RECIPIENT_IT_DWH],
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
            parameters=(CASE_TYPE_ID, GRAPHIC2_REDCAP_PROJECT_ID),
            schedule=Schedule.never,
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_case_link(
                row['StudyNumber'] or 'Click Here',
                row['civicrm_case_id'],
                row['civicrm_contact_id'],
            ))


class Graphic2RedcapNotInCiviCrm(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "are recruited in CiviCrm, but do not have "
                          "a record in REDCap"),
            recipients=[RECIPIENT_IT_DWH],
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
            parameters=(CASE_TYPE_ID, GRAPHIC2_REDCAP_PROJECT_ID),
            schedule=Schedule.never,
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_redcap_link(
                row['StudyNumber'] or 'Click Here',
                row['project_id'],
                row['StudyNumber'],
            ))

#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.connections import get_redcap_link
from reporter.uhl_reports.civicrm import get_case_link
from reporter.emailing import (
    RECIPIENT_IT_DWH
)


class DreamCivicrmNotInRedcap(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants "
                          "are recruited in CiviCrm, but do not have "
                          "a record in REDCap or Onyx"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''
                WITH c (StudyNumber, civicrm_case_id, civicrm_contact_id) AS (
                    SELECT  DISTINCT
                        i2b2ClinDataIntegration.dbo.ReplaceAll(UPPER(StudyNumber), ' DREAMB', '') StudyNumber,
                        civicrm_case_id,
                        civicrm_contact_id
                    FROM    STG_CiviCRM.dbo.LCBRU_CaseDetails
                    WHERE   case_type_id = 4
                        AND case_status_id IN (
                            5, -- Recruited
                            8, -- Withdrawn
                            9, -- Excluded
                            10 -- Completed
                        )
                        AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(StudyNumber) = 0
                ), r_int (StudyNumber) AS (
                    SELECT  DISTINCT
                        record AS StudyNumber
                    FROM    STG_redcap.dbo.redcap_data
                    WHERE project_id IN (8, 22)
                        AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(record) = 0
                )

                SELECT
                    StudyNumber,
                    civicrm_case_id,
                    civicrm_contact_id
                FROM c
                WHERE c.StudyNumber NOT IN (
                    SELECT StudyNumber
                    FROM r_int
                )
                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_case_link(
                row['StudyNumber'] or 'Click Here',
                row['civicrm_case_id'],
                row['civicrm_contact_id'],
            ))


class DreamRedcapNotInCiviCrm(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants "
                          "are recruited in REDCap, but do not have "
                          "a record in CiviCRM"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''
                WITH c (StudyNumber) AS (
                    SELECT  DISTINCT
                        i2b2ClinDataIntegration.dbo.ReplaceAll(UPPER(StudyNumber), ' DREAMB', '') StudyNumber
                    FROM    STG_CiviCRM.dbo.LCBRU_CaseDetails
                    WHERE   case_type_id = 4
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
                    WHERE project_id IN (8, 22)
                        AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(record) = 0
                )

                SELECT
                    StudyNumber,
                    project_id
                FROM r
                WHERE r.StudyNumber NOT IN (
                    SELECT StudyNumber
                    FROM c
                )
                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_redcap_link(
                row['StudyNumber'] or 'Click Here',
                row['project_id'],
                row['StudyNumber'],
            ))

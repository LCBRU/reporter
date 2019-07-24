#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.emailing import RECIPIENT_IT_DWH
from reporter.uhl_reports.civicrm import get_contact_id_search_link
from reporter.connections import get_redcap_link


class NationalBioresourceNotInCivicrm(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "a record in REDCap, but do not have "
                          "a record in CiviCRM"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

SELECT record
FROM STG_redcap.dbo.all_projects_fully_consented redcap
JOIN [STG_CiviCRM].[dbo].[LCBRU_CaseDetails] civi
	ON civi.case_type_id = 21
	AND civi.StudyNumber = 'National Bioresource'
	AND civi.is_recruited = 1
WHERE project_id = 9
    AND NOT EXISTS (
        SELECT 1
        FROM [STG_CiviCRM].[dbo].[LCBRU_CaseDetails] civi
        WHERE civi.case_type_id = 27
            AND (   civi.StudyNumber2 = redcap.record
                    OR  civi.StudyNumber3 = redcap.record)
    )

                '''
        )

    def get_report_line(self, row):
        return '- {}; {}\r\n'.format(
            get_redcap_link(
                row['record'],
                9,
                row['record'],
            ),
            get_contact_id_search_link(
                'CiviCRM',
                row['record'],
            ),
        )


class NationalCivicrmNotInBioresource(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "a record in CiviCRM, but do not have "
                          "a record in REDCap"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

DECLARE @redcap TABLE
(
  record VARCHAR(20) PRIMARY KEY
)

INSERT INTO @redcap(record)
SELECT DISTINCT record
FROM STG_redcap.dbo.all_projects_fully_consented redcap
		WHERE redcap.project_id = 9

SELECT StudyNumber
FROM [STG_CiviCRM].[dbo].[LCBRU_CaseDetails] civi
WHERE civi.case_type_id = 27
	AND NOT EXISTS (
		SELECT 1
		FROM @redcap redcap
		WHERE (StudyNumber2 = redcap.record
                    OR  civi.StudyNumber3 = redcap.record)
	)


                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_id_search_link(
                row['StudyNumber'],
                row['StudyNumber'],
        ))

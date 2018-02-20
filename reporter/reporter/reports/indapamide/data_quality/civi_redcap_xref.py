#!/usr/bin/env python3

from reporter.reports import SqlReport
from reporter.reports.emailing import RECIPIENT_INDAPAMIDE_ADMIN
from reporter.reports.redcap import get_redcap_link
from reporter.reports.civicrm import get_case_link


class IndapamideCivicrmNotInRedcap(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "are recruited in CiviCrm, but do not have "
                          "a record in REDCap"),
            recipients=[RECIPIENT_INDAPAMIDE_ADMIN],
            sql='''

SELECT c.CaseId,
        c.CiviCrmId,
        c.StudyNumber
FROM    i2b2_app03_indapamide_Data.dbo.LOAD_Civicrm c
WHERE NOT EXISTS (
    SELECT 1
    FROM i2b2_app03_indapamide_Data.dbo.LOAD_Redcap r
    WHERE r.StudyNumber = c.StudyNumber
)

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_case_link(
                row['StudyNumber'] or 'Click Here',
                row['CaseId'],
                row['CiviCrmId'],
            ))


class IndapamideRedcapNotInCiviCrm(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "are have full consent in REDCap, but are "
                          "not recruited in CiviCrm"),
            recipients=[RECIPIENT_INDAPAMIDE_ADMIN],
            sql='''

SELECT StudyNumber
FROM    i2b2_app03_indapamide_Data.dbo.LOAD_Redcap r
WHERE
    full_consent = 1
    AND NOT EXISTS (
        SELECT 1
        FROM i2b2_app03_indapamide_Data.dbo.LOAD_Civicrm c
        WHERE r.StudyNumber = c.StudyNumber
    )
                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_redcap_link(
                row['StudyNumber'] or 'Click Here',
                50,
                row['StudyNumber'],
            ))

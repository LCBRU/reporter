#!/usr/bin/env python3

from reporter.reports import SqlReport
from reporter.reports.emailing import RECIPIENT_IT_DWH
from reporter.reports.civicrm import get_contact_id_search_link


class BriccsRecruitsNotInRedcapOrOnyx(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "a record in CiviCRM, but do not have "
                          "a record in REDCap or Onyx"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

SELECT  studynumber, consent_date
FROM    i2b2_app03_b1_Data.dbo.LOAD_Civicrm a
WHERE NOT EXISTS (
        SELECT  1
        FROM    i2b2_app03_b1_Data.dbo.LOAD_Redcap
        WHERE   StudyNumber = a.StudyNumber
    ) AND NOT EXISTS (
        SELECT 1
        FROM i2b2_app03_b1_Data.dbo.LOAD_RedcapExternal
        WHERE StudyNumber = a.StudyNumber
    ) AND NOT EXISTS (
        SELECT  1
        FROM    i2b2_app03_b1_data.dbo.LOAD_Onyx
        WHERE   StudyNumber = a.StudyNumber
    )
    AND is_excluded = 0
    AND is_failed_to_respond = 0
    AND is_declined = 0
    AND is_recruitment_pending = 0
    AND is_duplicate = 0
    AND is_withdrawn = 0
    AND blank_study_id = 0

                '''
        )

    def get_report_line(self, row):
        return '- {} {}\r\n'.format(
            get_contact_id_search_link(
                row['studynumber'], row['studynumber']),
            '{:%d-%b-%Y}'.format(row['consent_date'])
            if row['consent_date'] else ''
        )

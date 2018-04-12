#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.emailing import RECIPIENT_IT_DWH
from reporter.uhl_reports.civicrm import get_contact_id_search_link


class BioresourceNotInRedcap(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "a record in CiviCRM, but do not have "
                          "a record in REDCap"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

SELECT  CONVERT(VARCHAR(100), bioresource_id) as bioresource_id, consent_date
FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Bioresource a
WHERE NOT EXISTS (
        SELECT  1
        FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Redcap_Bioresource
        WHERE   bioresource_id = a.bioresource_id
            OR bioresource_id = a.legacy_bioresource_id
    ) AND NOT EXISTS (
        SELECT 1
        FROM i2b2_app03_bioresource_Data.dbo.LOAD_Redcap_JointBriccs
        WHERE bioresource_id = a.bioresource_id
            OR bioresource_id = a.legacy_bioresource_id
    ) AND NOT EXISTS (
        SELECT  1
        FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Interval
        WHERE   bioresource_id = a.bioresource_id
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
                row['bioresource_id'], row['bioresource_id']),
            '{:%d-%b-%Y}'.format(row['consent_date'])
            if row['consent_date'] else ''
        )
